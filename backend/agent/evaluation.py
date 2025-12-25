from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import re


@dataclass
class EvaluationResult:
    """Result of the evaluation process."""
    quality_score: float
    issues: List[Dict[str, Any]]
    suggestions: List[str]
    confidence_in_evaluation: float


class EvaluationFramework:
    """Framework for evaluating agent responses for quality and accuracy."""

    def __init__(self):
        self.evaluation_rules = [
            self._check_hallucinations,
            self._check_context_leakage,
            self._check_factual_accuracy,
            self._check_relevance,
            self._check_coherence
        ]

    def evaluate_response(self, response: str, original_query: str, expected_context: Optional[str] = None) -> EvaluationResult:
        """Evaluate an agent response for quality and accuracy.

        Args:
            response: The response to evaluate
            original_query: The original query that generated the response
            expected_context: Expected context for the response (optional)

        Returns:
            EvaluationResult containing quality score and issues found
        """
        issues = []
        suggestions = []

        # Run all evaluation rules
        for rule in self.evaluation_rules:
            rule_issues, rule_suggestions = rule(response, original_query, expected_context)
            issues.extend(rule_issues)
            suggestions.extend(rule_suggestions)

        # Calculate quality score (higher is better, 1.0 is perfect)
        max_issues = 10  # Maximum possible issues for normalization
        issue_penalty = len(issues) / max_issues
        quality_score = max(0.0, 1.0 - issue_penalty)

        # Calculate confidence in evaluation
        confidence = self._calculate_evaluation_confidence(issues, response)

        return EvaluationResult(
            quality_score=quality_score,
            issues=issues,
            suggestions=suggestions,
            confidence_in_evaluation=confidence
        )

    def _check_hallucinations(self, response: str, original_query: str, expected_context: Optional[str]) -> tuple:
        """Check for hallucinations in the response.

        Args:
            response: The response to check
            original_query: The original query
            expected_context: Expected context for the response

        Returns:
            Tuple of (issues, suggestions)
        """
        issues = []
        suggestions = []

        # Look for common hallucination patterns
        # This is a simplified check - in practice, this would connect to a knowledge base
        if re.search(r'\b(according to .{0,20} source|cited in .{0,20} page|as mentioned in .{0,20} chapter)\b', response, re.IGNORECASE):
            # Check if the source actually exists in the context
            if expected_context and not self._validate_sources(response, expected_context):
                issues.append({
                    "type": "hallucination",
                    "description": "Response references sources that may not exist in the provided context",
                    "severity": "high"
                })
                suggestions.append("Only reference sources that are actually present in the provided context")

        # Check for overly confident statements about specific facts that can't be verified
        hallucination_patterns = [
            r'\bwas born on \w+ \d{1,2}, \d{4}\b',  # Specific dates that might be made up
            r'\baccording to page \d+ of\b',  # Page references without verification
            r'\bchapters? \d+ and \d+ state\b',  # Chapter references without verification
        ]

        for pattern in hallucination_patterns:
            if re.search(pattern, response, re.IGNORECASE):
                issues.append({
                    "type": "hallucination",
                    "description": f"Response contains specific details that may be fabricated: {re.search(pattern, response, re.IGNORECASE).group()}",
                    "severity": "high"
                })

        return issues, suggestions

    def _check_context_leakage(self, response: str, original_query: str, expected_context: Optional[str]) -> tuple:
        """Check for inappropriate context leakage.

        Args:
            response: The response to check
            original_query: The original query
            expected_context: Expected context for the response

        Returns:
            Tuple of (issues, suggestions)
        """
        issues = []
        suggestions = []

        # Check if response includes information that should be isolated
        # For example, if the agent was asked to analyze only selected text,
        # it should not include information from other parts of the book
        if 'selected text' in original_query.lower() or 'only this' in original_query.lower():
            # This would be checked against the actual context provided to the agent
            # For now, we'll look for general patterns
            if re.search(r'(other parts of the book|elsewhere|additionally|in chapter \w+)', response, re.IGNORECASE):
                issues.append({
                    "type": "context_leakage",
                    "description": "Response includes information from outside the specified context",
                    "severity": "medium"
                })
                suggestions.append("Stick to the provided context and avoid referencing other parts of the content")

        return issues, suggestions

    def _check_factual_accuracy(self, response: str, original_query: str, expected_context: Optional[str]) -> tuple:
        """Check for factual accuracy in the response.

        Args:
            response: The response to check
            original_query: The original query
            expected_context: Expected context for the response

        Returns:
            Tuple of (issues, suggestions)
        """
        issues = []
        suggestions = []

        # This is a simplified check - in practice, this would connect to a fact-checking system
        # For now, we'll look for patterns that might indicate factual issues
        contradiction_indicators = [
            r'(?i)\bboth .* and .* are correct\b',  # May indicate contradiction
            r'(?i)\bthis is always.*but sometimes\b',  # Contradictory statements
        ]

        for pattern in contradiction_indicators:
            if re.search(pattern, response):
                issues.append({
                    "type": "factual_error",
                    "description": f"Response may contain contradictory information: {re.search(pattern, response).group()}",
                    "severity": "medium"
                })

        return issues, suggestions

    def _check_relevance(self, response: str, original_query: str, expected_context: Optional[str]) -> tuple:
        """Check if the response is relevant to the query.

        Args:
            response: The response to check
            original_query: The original query
            expected_context: Expected context for the response

        Returns:
            Tuple of (issues, suggestions)
        """
        issues = []
        suggestions = []

        # Simple relevance check - look for query terms in response
        query_words = set(re.findall(r'\b\w+\b', original_query.lower()))
        response_words = set(re.findall(r'\b\w+\b', response.lower()))

        if query_words and response_words:
            overlap = len(query_words.intersection(response_words))
            total_query_words = len(query_words)

            # If less than 20% of query words appear in response, it might be irrelevant
            if total_query_words > 5 and (overlap / total_query_words) < 0.2:
                issues.append({
                    "type": "relevance",
                    "description": "Response appears to be minimally related to the original query",
                    "severity": "medium"
                })
                suggestions.append("Ensure the response directly addresses the query")

        return issues, suggestions

    def _check_coherence(self, response: str, original_query: str, expected_context: Optional[str]) -> tuple:
        """Check if the response is coherent and well-structured.

        Args:
            response: The response to check
            original_query: The original query
            expected_context: Expected context for the response

        Returns:
            Tuple of (issues, suggestions)
        """
        issues = []
        suggestions = []

        # Check for very short or very long responses
        words = response.split()
        if len(words) < 3:
            issues.append({
                "type": "coherence",
                "description": "Response is too brief to be informative",
                "severity": "low"
            })
            suggestions.append("Provide a more detailed response")

        # Check for apparent incoherence (too many conjunctions without clear structure)
        sentences = re.split(r'[.!?]+', response)
        for sentence in sentences:
            if len(sentence) > 200:  # Very long sentence
                issues.append({
                    "type": "coherence",
                    "description": f"Very long sentence detected: {sentence[:50]}...",
                    "severity": "low"
                })

        return issues, suggestions

    def _validate_sources(self, response: str, expected_context: str) -> bool:
        """Validate that sources mentioned in the response exist in the expected context.

        Args:
            response: The response containing source references
            expected_context: The context that should contain the sources

        Returns:
            True if sources are valid, False otherwise
        """
        # This is a simplified implementation
        # In practice, this would parse source references and validate them against the context
        return True  # Placeholder implementation

    def _calculate_evaluation_confidence(self, issues: List[Dict], response: str) -> float:
        """Calculate confidence in the evaluation results.

        Args:
            issues: List of issues found
            response: The response being evaluated

        Returns:
            Confidence score between 0 and 1
        """
        # Simple confidence calculation based on issue types and response length
        if not issues:
            return 1.0

        # Calculate based on issue severity
        severity_weights = {"low": 0.1, "medium": 0.3, "high": 0.5}
        total_weight = sum(severity_weights.get(issue["severity"], 0.1) for issue in issues)

        # Normalize by response length (longer responses might have more issues but also more content)
        length_factor = min(len(response.split()) / 100, 1.0)  # Cap at 1.0

        # Confidence decreases with more/serious issues, but increases with longer, more substantial responses
        confidence = max(0.1, 1.0 - total_weight + (length_factor * 0.1))
        return min(confidence, 1.0)


# Global evaluation framework instance
evaluation_framework = EvaluationFramework()


def evaluate_response(response: str, original_query: str, expected_context: Optional[str] = None) -> EvaluationResult:
    """Evaluate a response using the global evaluation framework.

    Args:
        response: The response to evaluate
        original_query: The original query that generated the response
        expected_context: Expected context for the response (optional)

    Returns:
        EvaluationResult containing quality score and issues found
    """
    return evaluation_framework.evaluate_response(response, original_query, expected_context)