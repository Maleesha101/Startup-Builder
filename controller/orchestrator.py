import asyncio
import os
import json
from typing import Dict
from .agents import (
    ProductAgent,
    ArchitectureAgent,
    TimelineAgent,
    FinanceAgent,
    MarketingAgent,
    AgentResult,
)


class Orchestrator:
    def __init__(self, output_dir: str = "output"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        self.product = ProductAgent()
        self.architecture = ArchitectureAgent()
        self.timeline = TimelineAgent()
        self.finance = FinanceAgent()
        self.marketing = MarketingAgent()

    async def run_workflow(self, idea: str) -> Dict[str, str]:
        results = {}

        # 1. Product Discovery
        print(f"Running Product Agent for idea: {idea}")
        product_res = await self.product.run({"idea": idea})
        self._save_artifact(product_res)
        results["product"] = product_res.output

        # 2. Architecture Design
        print("Running Architecture Agent...")
        arch_res = await self.architecture.run({"product_features": product_res.output})
        self._save_artifact(arch_res)
        results["architecture"] = arch_res.output

        # 3. Timeline Planning
        print("Running Timeline Agent...")
        timeline_res = await self.timeline.run(
            {"product_features": product_res.output, "architecture": arch_res.output}
        )
        self._save_artifact(timeline_res)
        results["timeline"] = timeline_res.output

        # 4. Finance & Marketing (Parallel)
        print("Running Finance and Marketing Agents...")
        finance_task = self.finance.run({"timeline": timeline_res.output})
        marketing_task = self.marketing.run(
            {"idea": idea, "product_features": product_res.output}
        )

        finance_res, marketing_res = await asyncio.gather(finance_task, marketing_task)
        self._save_artifact(finance_res)
        self._save_artifact(marketing_res)

        return {
            "product": product_res.artifact_content,
            "architecture": arch_res.artifact_content,
            "timeline": timeline_res.artifact_content,
            "finance": finance_res.artifact_content,
            "marketing": marketing_res.artifact_content,
        }

    def _save_artifact(self, result: AgentResult):
        path = os.path.join(self.output_dir, result.artifact_type)
        with open(path, "w", encoding="utf-8") as f:
            if isinstance(result.artifact_content, str):
                f.write(result.artifact_content)
            else:
                f.write(json.dumps(result.artifact_content, indent=2))
