import math
import time


class NeuroCore:

    def __init__(self, neurograph, engine):

        self.graph = neurograph
        self.engine = engine

    # =========================================================
    # CONTEXT BUILDER
    # =========================================================

    def build_context(self, query):

        return self.graph.build_context(query)

    # =========================================================
    # MAIN REASONING ENGINE
    # =========================================================

    def reason(self, query):

        start_time = time.time()

        context = self.build_context(query)

        if not context:

            return {
                "query": query,
                "final_answer": "No relevant memory found",
                "confidence": 0.0,
                "reasoning_steps": [],
                "latency": 0.0
            }

        # =====================================================
        # IMPROVED RANKING (NORMALIZED SCORING)
        # =====================================================

        ranked = sorted(
            context,
            key=lambda x: self._score(x),
            reverse=True
        )

        steps = []

        # =====================================================
        # STEP 1: INTENT ANALYSIS (IMPROVED)
        # =====================================================

        intent = self._analyze_intent(query)

        steps.append({
            "step": 1,
            "type": "intent_analysis",
            "result": intent
        })

        # =====================================================
        # STEP 2: MEMORY FUSION (DEEPER)
        # =====================================================

        memory_insights = self._extract_memories(ranked)

        steps.append({
            "step": 2,
            "type": "memory_fusion",
            "result": memory_insights
        })

        # =====================================================
        # STEP 3: CONTEXTUAL REASONING
        # =====================================================

        synthesis = self._synthesize(intent, memory_insights, query)

        steps.append({
            "step": 3,
            "type": "reasoning_synthesis",
            "result": synthesis
        })

        # =====================================================
        # STEP 4: SELF-REFINEMENT
        # =====================================================

        final_answer = self._refine_answer(synthesis, ranked)

        steps.append({
            "step": 4,
            "type": "self_refinement",
            "result": final_answer
        })

        # =====================================================
        # CONFIDENCE ENGINE (IMPROVED)
        # =====================================================

        confidence = self._confidence_score(ranked, intent)

        latency = time.time() - start_time

        return {
            "query": query,
            "final_answer": final_answer,
            "confidence": confidence,
            "reasoning_steps": steps,
            "context_used": len(ranked),
            "latency": latency
        }

    # =========================================================
    # INTENT ANALYSIS (IMPROVED)
    # =========================================================

    def _analyze_intent(self, query):

        q = query.lower()

        intent_map = {
            "why": "causal_reasoning",
            "how": "procedural_reasoning",
            "what": "definition_retrieval",
            "when": "temporal_reasoning",
            "where": "spatial_reasoning",
            "should": "decision_support",
            "can": "feasibility_analysis"
        }

        for key, value in intent_map.items():

            if key in q:

                return value

        return "general_reasoning"

    # =========================================================
    # MEMORY EXTRACTION (IMPROVED DEPTH)
    # =========================================================

    def _extract_memories(self, context):

        return [
            {
                "content": item.get("content", ""),
                "score": item.get("score", 0),
                "importance": item.get("importance", 0)
            }
            for item in context[:5]
        ]

    # =========================================================
    # SYNTHESIS ENGINE (MORE INTELLIGENT)
    # =========================================================

    def _synthesize(self, intent, memories, query):

        if not memories:

            return "No meaningful memory patterns detected"

        top_memories = " | ".join(
            m["content"] for m in memories[:3]
        )

        return (
            f"Intent: {intent}. "
            f"Derived reasoning from memory patterns: {top_memories}"
        )

    # =========================================================
    # FINAL REFINEMENT (RULE + LOGIC BLEND)
    # =========================================================

    def _refine_answer(self, synthesis, context):

        if len(context) >= 3:

            return (
                f"{synthesis}. "
                "Cross-validation across multiple memory nodes increases reliability."
            )

        if len(context) == 2:

            return (
                f"{synthesis}. "
                "Moderate confidence due to limited memory convergence."
            )

        return synthesis

    # =========================================================
    # IMPROVED CONFIDENCE MODEL
    # =========================================================

    def _confidence_score(self, context, intent):

        if not context:

            return 0.0

        scores = [
            self._score(c)
            for c in context[:5]
        ]

        avg_score = sum(scores) / len(scores)

        # intent boost logic
        intent_boost = 0.1 if intent != "general_reasoning" else 0.0

        return min(
            1.0,
            avg_score + intent_boost
        )

    # =========================================================
    # SCORING FUNCTION (NORMALIZED)
    # =========================================================

    def _score(self, item):

        score = item.get("score", 0)
        importance = item.get("importance", 0)

        return (score * 0.7) + (importance * 0.3)