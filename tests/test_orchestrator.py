import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from controller.orchestrator import Orchestrator
from controller.agents import AgentResult


@pytest.fixture
def mock_agents():
    with (
        patch("controller.orchestrator.ProductAgent") as MockProduct,
        patch("controller.orchestrator.ArchitectureAgent") as MockArch,
        patch("controller.orchestrator.TimelineAgent") as MockTimeline,
        patch("controller.orchestrator.FinanceAgent") as MockFinance,
        patch("controller.orchestrator.MarketingAgent") as MockMarketing,
    ):
        # Setup mocks
        for MockClass in [
            MockProduct,
            MockArch,
            MockTimeline,
            MockFinance,
            MockMarketing,
        ]:
            instance = MockClass.return_value
            instance.run = AsyncMock(
                return_value=AgentResult(
                    agent_name="Mock",
                    output={"mock": "data"},
                    artifact_type="test.json",
                    artifact_content="{}",
                )
            )

        yield {
            "product": MockProduct,
            "arch": MockArch,
            "timeline": MockTimeline,
            "finance": MockFinance,
            "marketing": MockMarketing,
        }


@pytest.mark.asyncio
async def test_orchestrator_flow(mock_agents):
    orchestrator = Orchestrator(output_dir="test_output")

    # Run
    results = await orchestrator.run_workflow("Test Idea")

    # Verify calls
    mock_agents["product"].return_value.run.assert_called_once()
    mock_agents["arch"].return_value.run.assert_called_once()
    mock_agents["timeline"].return_value.run.assert_called_once()
    # Check that they ran
    assert "product" in results
    assert "finance" in results
