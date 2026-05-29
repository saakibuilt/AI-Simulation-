

import json
import logging
import re
from typing import Dict, Any, List, Optional
from ..utils.llm_client import LLMClient
from ..utils.locale import get_language_instruction

logger = logging.getLogger(__name__)


def _to_pascal_case(name: str) -> str:
    
    
    parts = re.split(r'[^a-zA-Z0-9]+', name)
    
    words = []
    for part in parts:
        words.extend(re.sub(r'([a-z])([A-Z])', r'\1_\2', part).split('_'))
    
    result = ''.join(word.capitalize() for word in words if word)
    return result if result else 'Unknown'



ONTOLOGY_SYSTEM_PROMPT = """You are an expert knowledge-graph ontology designer. Analyze the provided documents and simulation requirement, then design entity types and relationship types suitable for a **social media opinion simulation**.

**Important: you must return valid JSON only. Do not return any extra text.**

## Core task background

We are building a **social media opinion simulation system**. In this system:
- Every entity should be a real-world actor that can post, react, interact, or spread information on social platforms.
- Entities influence each other through reposts, comments, replies, endorsements, and criticism.
- We need to model reaction patterns and information propagation during public discussion events.

Therefore, **entities must be real-world actors that can reasonably speak and interact on social media**.

**Allowed examples**:
- Specific individuals such as public figures, participants, influencers, experts, or ordinary people
- Companies and businesses, including their official accounts
- Organizations such as universities, associations, NGOs, and unions
- Government agencies and regulators
- Media organizations such as newspapers, TV stations, independent media, or websites
- Social media platforms themselves
- Representative groups such as alumni associations, fan communities, or advocacy groups

**Disallowed examples**:
- Abstract concepts such as "public opinion", "emotion", or "trend"
- Topics or issues such as "academic integrity" or "education reform"
- Positions or attitudes such as "supporters" or "opponents"

## Output format

Return JSON with the following structure:

```json
{
    "entity_types": [
        {
            "name": "Entity type name in English PascalCase",
            "description": "Short description in English, under 100 characters",
            "attributes": [
                {
                    "name": "Attribute name in English snake_case",
                    "type": "text",
                    "description": "Attribute description"
                }
            ],
            "examples": ["Example entity 1", "Example entity 2"]
        }
    ],
    "edge_types": [
        {
            "name": "Relationship type name in English UPPER_SNAKE_CASE",
            "description": "Short description in English, under 100 characters",
            "source_targets": [
                {"source": "Source entity type", "target": "Target entity type"}
            ],
            "attributes": []
        }
    ],
    "analysis_summary": "Brief analysis summary of the content"
}
```

## Design rules

### 1. Entity type design

**You must return exactly 10 entity types.**

**Hierarchy requirement: include both specific types and fallback types.**

Your 10 entity types must include the following:

A. **Fallback types (required, place them as the last 2 items)**:
   - `Person`: fallback type for any natural person not covered by a more specific person type.
   - `Organization`: fallback type for any organization not covered by a more specific organization type.

B. **Specific types (8 types, derived from the content)**:
   - Design more specific types for the major roles in the documents.
   - Example for an academic event: `Student`, `Professor`, `University`
   - Example for a business event: `Company`, `CEO`, `Employee`

**Why fallback types are required**:
- The documents may mention many people who do not fit a specialized role.
- Those people should be categorized as `Person`.
- Likewise, small organizations or temporary groups should be categorized as `Organization`.

**Specific type design principles**:
- Focus on frequent or important role categories found in the documents.
- Each specific type should have clear boundaries and minimal overlap.
- Each description must explain how the type differs from the fallback type.

### 2. Relationship type design

- Return 6 to 10 relationship types.
- Relationship types should reflect realistic social or informational connections.
- Ensure `source_targets` are compatible with the entity types you define.

### 3. Attribute design

- Each entity type should have 1 to 3 key attributes.
- **Do not use** reserved attribute names such as `name`, `uuid`, `group_id`, `created_at`, or `summary`.
- Good options include `full_name`, `title`, `role`, `position`, `location`, and `description`.

## Example entity types

**Specific person types**:
- Student
- Professor
- Journalist
- Celebrity
- Executive
- Official
- Lawyer
- Doctor

**Fallback person type**:
- Person

**Specific organization types**:
- University
- Company
- GovernmentAgency
- MediaOutlet
- Hospital
- School
- NGO

**Fallback organization type**:
- Organization

## Example relationship types

- WORKS_FOR
- STUDIES_AT
- AFFILIATED_WITH
- REPRESENTS
- REGULATES
- REPORTS_ON
- COMMENTS_ON
- RESPONDS_TO
- SUPPORTS
- OPPOSES
- COLLABORATES_WITH
- COMPETES_WITH
"""


class OntologyGenerator:
    
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        self.llm_client = llm_client or LLMClient()
    
    def generate(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str] = None
    ) -> Dict[str, Any]:
        
        
        user_message = self._build_user_message(
            document_texts, 
            simulation_requirement,
            additional_context
        )
        
        lang_instruction = get_language_instruction()
        system_prompt = f"{ONTOLOGY_SYSTEM_PROMPT}\n\n{lang_instruction}\nIMPORTANT: Entity type names MUST be in English PascalCase (e.g., 'PersonEntity', 'MediaOrganization'). Relationship type names MUST be in English UPPER_SNAKE_CASE (e.g., 'WORKS_FOR'). Attribute names MUST be in English snake_case. Only description fields and analysis_summary should use the specified language above."
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_message}
        ]
        
        
        result = self.llm_client.chat_json(
            messages=messages,
            temperature=0.3,
            max_tokens=4096
        )
        
        
        result = self._validate_and_process(result)
        
        return result
    
    
    MAX_TEXT_LENGTH_FOR_LLM = 50000
    
    def _build_user_message(
        self,
        document_texts: List[str],
        simulation_requirement: str,
        additional_context: Optional[str]
    ) -> str:
        
        
        
        combined_text = "\n\n---\n\n".join(document_texts)
        original_length = len(combined_text)
        
        
        if len(combined_text) > self.MAX_TEXT_LENGTH_FOR_LLM:
            combined_text = combined_text[:self.MAX_TEXT_LENGTH_FOR_LLM]
            combined_text += (
                f"\n\n...(Original text length: {original_length} characters. "
                f"Only the first {self.MAX_TEXT_LENGTH_FOR_LLM} characters were used for ontology analysis.)..."
            )
        
        message = f"""## Simulation Requirement

{simulation_requirement}

## Document Content

{combined_text}
"""
        
        if additional_context:
            message += f"""
## Additional Context

{additional_context}
"""
        
        message += """
Please design entity types and relationship types appropriate for a social opinion simulation based on the content above.

**Rules you must follow**:
1. Return exactly 10 entity types.
2. The last 2 entity types must be the fallback types: `Person` and `Organization`.
3. The first 8 entity types must be specific types derived from the documents.
4. Every entity type must represent a real-world actor that can communicate, not an abstract concept.
5. Do not use reserved attribute names such as `name`, `uuid`, or `group_id`; use names like `full_name` or `org_name` instead.
"""
        
        return message
    
    def _validate_and_process(self, result: Dict[str, Any]) -> Dict[str, Any]:
        
        
        
        if "entity_types" not in result:
            result["entity_types"] = []
        if "edge_types" not in result:
            result["edge_types"] = []
        if "analysis_summary" not in result:
            result["analysis_summary"] = ""
        
        
        
        entity_name_map = {}
        for entity in result["entity_types"]:
            
            if "name" in entity:
                original_name = entity["name"]
                entity["name"] = _to_pascal_case(original_name)
                if entity["name"] != original_name:
                    logger.warning(f"Entity type name '{original_name}' auto-converted to '{entity['name']}'")
                entity_name_map[original_name] = entity["name"]
            if "attributes" not in entity:
                entity["attributes"] = []
            if "examples" not in entity:
                entity["examples"] = []
            
            if len(entity.get("description", "")) > 100:
                entity["description"] = entity["description"][:97] + "..."
        
        
        for edge in result["edge_types"]:
            
            if "name" in edge:
                original_name = edge["name"]
                edge["name"] = original_name.upper()
                if edge["name"] != original_name:
                    logger.warning(f"Edge type name '{original_name}' auto-converted to '{edge['name']}'")
            
            for st in edge.get("source_targets", []):
                if st.get("source") in entity_name_map:
                    st["source"] = entity_name_map[st["source"]]
                if st.get("target") in entity_name_map:
                    st["target"] = entity_name_map[st["target"]]
            if "source_targets" not in edge:
                edge["source_targets"] = []
            if "attributes" not in edge:
                edge["attributes"] = []
            if len(edge.get("description", "")) > 100:
                edge["description"] = edge["description"][:97] + "..."
        
        
        MAX_ENTITY_TYPES = 10
        MAX_EDGE_TYPES = 10

        
        seen_names = set()
        deduped = []
        for entity in result["entity_types"]:
            name = entity.get("name", "")
            if name and name not in seen_names:
                seen_names.add(name)
                deduped.append(entity)
            elif name in seen_names:
                logger.warning(f"Duplicate entity type '{name}' removed during validation")
        result["entity_types"] = deduped

        
        person_fallback = {
            "name": "Person",
            "description": "Any individual person not fitting other specific person types.",
            "attributes": [
                {"name": "full_name", "type": "text", "description": "Full name of the person"},
                {"name": "role", "type": "text", "description": "Role or occupation"}
            ],
            "examples": ["ordinary citizen", "anonymous netizen"]
        }
        
        organization_fallback = {
            "name": "Organization",
            "description": "Any organization not fitting other specific organization types.",
            "attributes": [
                {"name": "org_name", "type": "text", "description": "Name of the organization"},
                {"name": "org_type", "type": "text", "description": "Type of organization"}
            ],
            "examples": ["small business", "community group"]
        }
        
        
        entity_names = {e["name"] for e in result["entity_types"]}
        has_person = "Person" in entity_names
        has_organization = "Organization" in entity_names
        
        
        fallbacks_to_add = []
        if not has_person:
            fallbacks_to_add.append(person_fallback)
        if not has_organization:
            fallbacks_to_add.append(organization_fallback)
        
        if fallbacks_to_add:
            current_count = len(result["entity_types"])
            needed_slots = len(fallbacks_to_add)
            
            
            if current_count + needed_slots > MAX_ENTITY_TYPES:
                
                to_remove = current_count + needed_slots - MAX_ENTITY_TYPES
                
                result["entity_types"] = result["entity_types"][:-to_remove]
            
            
            result["entity_types"].extend(fallbacks_to_add)
        
        
        if len(result["entity_types"]) > MAX_ENTITY_TYPES:
            result["entity_types"] = result["entity_types"][:MAX_ENTITY_TYPES]
        
        if len(result["edge_types"]) > MAX_EDGE_TYPES:
            result["edge_types"] = result["edge_types"][:MAX_EDGE_TYPES]
        
        return result
    
    def generate_python_code(self, ontology: Dict[str, Any]) -> str:
        
        code_lines = [
            '"""',
            'Custom entity type definitions',
            'Auto-generated by Analytics Fish for social opinion simulation',
            '"""',
            '',
            'from pydantic import Field',
            'from zep_cloud.external_clients.ontology import EntityModel, EntityText, EdgeModel',
            '',
            '',
            '# ============== Entity Type Definitions ==============',
            '',
        ]
        
        
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            desc = entity.get("description", f"A {name} entity.")
            
            code_lines.append(f'class {name}(EntityModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = entity.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        code_lines.append('# ============== Relationship Type Definitions ==============')
        code_lines.append('')
        
        
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            desc = edge.get("description", f"A {name} relationship.")
            
            code_lines.append(f'class {class_name}(EdgeModel):')
            code_lines.append(f'    """{desc}"""')
            
            attrs = edge.get("attributes", [])
            if attrs:
                for attr in attrs:
                    attr_name = attr["name"]
                    attr_desc = attr.get("description", attr_name)
                    code_lines.append(f'    {attr_name}: EntityText = Field(')
                    code_lines.append(f'        description="{attr_desc}",')
                    code_lines.append(f'        default=None')
                    code_lines.append(f'    )')
            else:
                code_lines.append('    pass')
            
            code_lines.append('')
            code_lines.append('')
        
        
        code_lines.append('# ============== Type Registry ==============')
        code_lines.append('')
        code_lines.append('ENTITY_TYPES = {')
        for entity in ontology.get("entity_types", []):
            name = entity["name"]
            code_lines.append(f'    "{name}": {name},')
        code_lines.append('}')
        code_lines.append('')
        code_lines.append('EDGE_TYPES = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            class_name = ''.join(word.capitalize() for word in name.split('_'))
            code_lines.append(f'    "{name}": {class_name},')
        code_lines.append('}')
        code_lines.append('')
        
        
        code_lines.append('EDGE_SOURCE_TARGETS = {')
        for edge in ontology.get("edge_types", []):
            name = edge["name"]
            source_targets = edge.get("source_targets", [])
            if source_targets:
                st_list = ', '.join([
                    f'{{"source": "{st.get("source", "Entity")}", "target": "{st.get("target", "Entity")}"}}'
                    for st in source_targets
                ])
                code_lines.append(f'    "{name}": [{st_list}],')
        code_lines.append('}')
        
        return '\n'.join(code_lines)
