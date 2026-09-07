from agents import Runner
from incident_analyzer.utils import logger

from incident_analyzer.models import IncidentAnalysis,IncidentRequest
from incident_analyzer.incident_agent import incident_agent


def analyze_incident(request: IncidentRequest) -> IncidentAnalysis:
    try:

        result= Runner.run_sync(incident_agent,request.description)

        return result.final_output

    except Exception as e:
        logger.error(f"LLM call failed: {e}")

        logger.warning("[Notice] Api fail mock response---")

        return IncidentAnalysis(
        category="Application",
        severity="High",
        summary="summary ",
        next_action="Fix issues"

        )

def main():
    try:
        incident_id =int(input("Enter incident id: "))
        description = input("Enter incident description: ")

        incident=IncidentRequest(
            incident_id=incident_id,
            description=description
            )

        result=analyze_incident(incident)
        print("Incident analysis")
        print(result)

    except Exception as e:
        logger.error("error occured in main")
        print("Error:", e)

if __name__=="__main__":
    main()