import backoff
import openai
from .pricing import OPENAI_MODELS
from .result import QueryResult
import logging

logger = logging.getLogger(__name__)


def backoff_handler(details):
    exc = details.get("exception")
    if exc:
        logger.warning(
            f"OpenAI - Retry {details['tries']} due to error: {exc}. Waiting {details['wait']:0.1f}s..."
        )


@backoff.on_exception(
    backoff.expo,
    (
        openai.APIConnectionError,
        openai.APIStatusError,
        openai.RateLimitError,
        openai.APITimeoutError,
    ),
    max_tries=20,
    max_value=20,
    on_backoff=backoff_handler,
)
def query_openai(
    client,
    model,
    msg,
    system_msg,
    msg_history,
    output_model,
    model_posteriors=None,
    **kwargs,
) -> QueryResult:
    """Query OpenAI model."""
    new_msg_history = msg_history + [{"role": "user", "content": msg}]
    if output_model is None:
        response = client.responses.create(
            model=model,
            input=[
                {"role": "system", "content": system_msg},
                *new_msg_history,
            ],
            **kwargs,
        )
        try:
            content = response.output[0].content[0].text
        except Exception:
            # Reasoning models - ResponseOutputMessage
            content = response.output[1].content[0].text
        new_msg_history.append({"role": "assistant", "content": content})
    else:
        response = client.responses.parse(
            model=model,
            input=[
                {"role": "system", "content": system_msg},
                *new_msg_history,
            ],
            text_format=output_model,
            **kwargs,
        )
        content = response.output_parsed
        new_content = ""
        for i in content:
            # Handle case where i[1] might be a list or other type
            if isinstance(i[1], list):
                value_str = ", ".join(str(x) for x in i[1])
            else:
                value_str = str(i[1])
            new_content += i[0] + ":" + value_str + "\n"
        new_msg_history.append({"role": "assistant", "content": new_content})

    input_cost = OPENAI_MODELS[model]["input_price"] * response.usage.input_tokens
    output_cost = OPENAI_MODELS[model]["output_price"] * response.usage.output_tokens
    # For structured output, try to parse the content into Pydantic model
    parsed_content_obj = None
    if output_model is not None and content:
        logger.debug(f"Structured output: content type={type(content)}, model={output_model.__name__}")
        logger.debug(f"Structured output: content preview={str(content)[:300]}")
        try:
            # Check if content is already a Pydantic model instance
            if isinstance(content, output_model):
                logger.debug(f"Structured output: Content is already {output_model.__name__} instance")
                parsed_content_obj = content
            elif isinstance(content, list):
                logger.debug(f"Structured output: Processing list with {len(content)} items")
                # Convert list of key-value pairs to dict
                content_dict = {}
                for item in content:
                    if len(item) >= 2:
                        key, value = item[0], item[1]
                        content_dict[key] = value
                        logger.debug(f"Structured output: Added {key}={value}")
                logger.debug(f"Structured output: Final dict={content_dict}")
                parsed_content_obj = output_model(**content_dict)
                logger.debug(f"Structured output: Successfully created {output_model.__name__}")
            elif isinstance(content, str):
                logger.debug("Structured output: Processing string content")
                # Try to parse as JSON
                import json
                content_dict = json.loads(content)
                logger.debug(f"Structured output: Parsed JSON dict={content_dict}")
                parsed_content_obj = output_model(**content_dict)
                logger.debug(f"Structured output: Successfully created {output_model.__name__}")
            else:
                logger.debug(f"Structured output: Unexpected content type {type(content)}")
        except Exception as e:
            logger.warning(f"Failed to parse structured output into {output_model.__name__}: {e}")
            logger.debug(f"Structured output error details: content={content}")

    result = QueryResult(
        content=content,
        msg=msg,
        system_msg=system_msg,
        new_msg_history=new_msg_history,
        model_name=model,
        kwargs=kwargs,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        cost=input_cost + output_cost,
        input_cost=input_cost,
        output_cost=output_cost,
        thought="",
        model_posteriors=model_posteriors,
        parsed_content=parsed_content_obj,
    )
    return result
