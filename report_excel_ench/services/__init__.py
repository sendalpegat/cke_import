from . import excel_generator
from . import template_processor
from . import data_processor
from . import formula_evaluator
from . import cache_service
from . import streaming_processor

# Service registry for dependency injection
SERVICE_REGISTRY = {
    'excel_generator': excel_generator.ExcelGeneratorService,
    'template_processor': template_processor.TemplateProcessorService,
    'data_processor': data_processor.DataProcessorService,
    'formula_evaluator': formula_evaluator.FormulaEvaluatorService,
    'cache_service': cache_service.CacheService,
    'streaming_processor': streaming_processor.StreamingDataProcessor,
}

def get_service(service_name, env):
    """Get service instance"""
    service_class = SERVICE_REGISTRY.get(service_name)
    if not service_class:
        raise ValueError(f"Service '{service_name}' not found")
    return service_class(env)