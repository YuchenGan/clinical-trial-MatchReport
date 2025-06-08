import httpx
import asyncio
from typing import List, Dict, Optional
import logging

# Set up logging
logger = logging.getLogger(__name__)

RELEVANT_STATUSES = {"RECRUITING", "NOT_YET_RECRUITING"}


async def search_trials_basic(condition: str, max_results: Optional[int] = None) -> List[Dict]:
    """
    Basic clinical trial search with unlimited results support

    Args:
        condition: Search condition (disease name, gene mutation, etc.)
        max_results: Maximum results to return, None for unlimited

    Returns:
        List of recruiting clinical trials
    """

    logger.info(f"Searching clinical trials: {condition}, max results: {max_results or 'unlimited'}")

    all_trials = []
    page_size = 1000  # Maximum per page
    page_token = None
    total_fetched = 0

    async with httpx.AsyncClient(timeout=30) as client:
        while True:
            try:
                # Build request parameters
                params = {
                    "query.term": condition,
                    "pageSize": page_size,
                    "format": "json"
                }

                # Add pagination token if available
                if page_token:
                    params["pageToken"] = page_token

                # Make API request
                response = await client.get(
                    "https://clinicaltrials.gov/api/v2/studies",
                    params=params
                )
                response.raise_for_status()
                data = response.json()

                # Extract studies
                studies = data.get("studies", [])
                if not studies:
                    logger.info(f"No more trial data found, stopping pagination")
                    break

                # Filter for recruiting trials
                recruiting_trials = filter_recruiting_trials(studies)
                all_trials.extend(recruiting_trials)
                total_fetched += len(recruiting_trials)

                logger.info(f"Fetched {len(recruiting_trials)} recruiting trials this page, total: {total_fetched}")

                # Check if we've reached the maximum results limit
                if max_results and total_fetched >= max_results:
                    all_trials = all_trials[:max_results]
                    logger.info(f"Reached maximum results limit {max_results}, stopping search")
                    break

                # Check if there's a next page
                next_page_token = data.get("nextPageToken")
                if not next_page_token:
                    logger.info("No more pages available, search complete")
                    break

                page_token = next_page_token

                # Add small delay to avoid rate limiting
                await asyncio.sleep(0.1)

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error {e.response.status_code}: {e.response.text}")
                if e.response.status_code == 429:  # Rate limited
                    logger.info("Rate limited, waiting 3 seconds before retry...")
                    await asyncio.sleep(3)
                    continue
                else:
                    raise
            except Exception as e:
                logger.error(f"Error searching for '{condition}': {str(e)}")
                break

    logger.info(f"Search complete: {condition} -> {len(all_trials)} recruiting trials")
    return all_trials


def filter_recruiting_trials(studies: List[Dict]) -> List[Dict]:
    """Filter studies to only include those that are recruiting"""
    recruiting_trials = []

    for trial in studies:
        try:
            status = trial.get("protocolSection", {}).get("statusModule", {}).get("overallStatus", "")
            if status in RELEVANT_STATUSES:
                recruiting_trials.append(trial)
        except Exception as e:
            logger.warning(f"Error parsing trial status: {str(e)}")
            continue

    return recruiting_trials


async def search_trials_batch(search_queries: List[str], max_results_per_query: Optional[int] = None) -> Dict[
    str, List[Dict]]:
    """
    Batch search multiple conditions in parallel

    Args:
        search_queries: List of search conditions
        max_results_per_query: Maximum results per query

    Returns:
        Dictionary mapping query to trial list
    """

    logger.info(f"Starting batch search for {len(search_queries)} queries")

    # Create concurrent tasks
    tasks = []
    for query in search_queries:
        task = search_trials_basic(query, max_results_per_query)
        tasks.append((query, task))

    # Execute all searches concurrently
    results = {}
    completed_tasks = await asyncio.gather(
        *[task for _, task in tasks],
        return_exceptions=True
    )

    # Process results
    for (query, _), result in zip(tasks, completed_tasks):
        if isinstance(result, Exception):
            logger.error(f"Query '{query}' failed: {str(result)}")
            results[query] = []
        else:
            results[query] = result
            logger.info(f"Query '{query}' successful: {len(result)} trials")

    return results


async def get_trial_details(nct_id: str) -> Optional[Dict]:
    """
    Get detailed information for a specific trial

    Args:
        nct_id: Clinical trial NCT ID

    Returns:
        Detailed trial information or None
    """

    try:
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.get(
                f"https://clinicaltrials.gov/api/v2/studies/{nct_id}",
                params={"format": "json"}
            )
            response.raise_for_status()
            data = response.json()

            return data.get("protocolSection", {})

    except Exception as e:
        logger.error(f"Failed to get trial details for {nct_id}: {str(e)}")
        return None


async def search_trials_with_geo_filter(
        condition: str,
        country: str = "United States",
        max_results: Optional[int] = None
) -> List[Dict]:
    """
    Search trials with geographic filtering

    Args:
        condition: Search condition
        country: Country to filter by
        max_results: Maximum results

    Returns:
        Filtered trial list
    """

    # Add geographic filter to search condition
    geo_condition = f"{condition} AND AREA[LocationCountry]{country}"

    return await search_trials_basic(geo_condition, max_results)


def merge_and_deduplicate_trials(trial_lists: List[List[Dict]]) -> List[Dict]:
    """
    Merge multiple trial lists and remove duplicates

    Args:
        trial_lists: List of trial lists to merge

    Returns:
        Deduplicated merged trial list
    """

    seen_nct_ids = set()
    merged_trials = []

    for trial_list in trial_lists:
        for trial in trial_list:
            try:
                nct_id = trial.get("protocolSection", {}).get("identificationModule", {}).get("nctId", "")
                if nct_id and nct_id not in seen_nct_ids:
                    seen_nct_ids.add(nct_id)
                    merged_trials.append(trial)
            except Exception as e:
                logger.warning(f"Error processing trial data: {str(e)}")
                continue

    logger.info(f"Merge and deduplication complete: {len(merged_trials)} unique trials")
    return merged_trials


def analyze_search_results(trials: List[Dict], search_term: str) -> Dict:
    """
    Analyze search result quality

    Args:
        trials: Trial list
        search_term: Original search term

    Returns:
        Analysis statistics
    """

    if not trials:
        return {
            "total_count": 0,
            "quality": "no_results",
            "recommendations": ["Try broader search terms", "Check spelling"]
        }

    # Analyze relevance
    title_matches = 0
    search_lower = search_term.lower()

    for trial in trials:
        try:
            title = trial.get("protocolSection", {}).get("identificationModule", {}).get("officialTitle", "").lower()

            if search_lower in title:
                title_matches += 1

        except Exception:
            continue

    total = len(trials)
    title_relevance = title_matches / total if total > 0 else 0

    # Quality assessment
    if title_relevance > 0.3:
        quality = "excellent"
    elif title_relevance > 0.15:
        quality = "good"
    elif title_relevance > 0.05:
        quality = "fair"
    else:
        quality = "poor"

    return {
        "total_count": total,
        "title_matches": title_matches,
        "title_relevance": round(title_relevance, 3),
        "quality": quality,
        "search_term": search_term
    }


# Additional utility functions for data extraction
def get_trial_conditions(trial: Dict) -> List[str]:
    """
    Extract conditions/diseases from a trial
    """
    try:
        conditions_module = trial.get("protocolSection", {}).get("conditionsModule", {})
        return conditions_module.get("conditions", [])
    except Exception:
        return []


def get_trial_interventions(trial: Dict) -> List[str]:
    """
    Extract intervention names from a trial
    """
    try:
        interventions_module = trial.get("protocolSection", {}).get("armsInterventionsModule", {})
        interventions = interventions_module.get("interventions", [])
        return [intervention.get("name", "") for intervention in interventions]
    except Exception:
        return []


def generate_clinicaltrials_url(nct_id: str) -> str:
    """
    Generate standardized ClinicalTrials.gov URL

    Args:
        nct_id: Clinical trial NCT ID

    Returns:
        Full URL to trial details page
    """
    return f"https://clinicaltrials.gov/ct2/show/{nct_id}"