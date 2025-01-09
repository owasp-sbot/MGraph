# Python Code Formatting Specification

## Import Statements
Imports should be aligned with the longest import path, using spaces between major groups:

```python
from unittest                                        import TestCase
from mgraph_ai.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Node__Config  import Schema__MGraph__Node__Config
from mgraph_ai.schemas.Schema__MGraph__Attribute     import Schema__MGraph__Attribute
from osbot_utils.helpers.Random_Guid                 import Random_Guid
from osbot_utils.helpers.Safe_Id                     import Safe_Id
```

## Method Documentation
Method documentation should be provided as inline comments on the same line as the method definition at the same column (starting on 80):

```python
def setUp(self):                                                               # Initialize test data
def test_init(self):                                                           # Tests basic initialization and type checking
```

## Variable Assignment Alignment
Variable assignments should be aligned on the `=` operator:

```python
self.node_id    = Random_Guid()
self.value_type = str
self.attribute  = Schema__MGraph__Attribute(...)
```

## Constructor Calls
Constructor calls should be formatted with aligned parameters, aligned equals signs, and aligned commas:

```python
node_config = Schema__MGraph__Node__Config(node_id    = Random_Guid(),
                                           value_type = str          )

attribute  = Schema__MGraph__Attribute(attribute_id    = Random_Guid()    ,
                                       attribute_name  = Safe_Id('attr_1'),
                                       attribute_value = "value_1"        ,
                                       attribute_type  = str              )
```

Note that:
- The opening parenthesis is on the same line as the constructor call
- Parameters are indented to align with the start of the constructor name
- Equals signs are aligned
- Commas are aligned at the end
- Closing parenthesis is aligned with the commas

## Assert Statements
Assert statements should be aligned on the comparison operator:

```python
assert type(self.node)                                   is Schema__MGraph__Node
assert self.node.node_config                             == self.node_config
assert self.node.value                                   == "test_node_value"
assert len(self.node.attributes)                         == 1
assert self.node.attributes[self.attribute.attribute_id] == self.attribute
```

## Dictionary Literals
Dictionary literals in constructor calls should maintain alignment while using minimal line breaks:

```python
node = Schema__MGraph__Node(attributes = {attr_1.attribute_id: attr_1 ,
                                          attr_2.attribute_id: attr_2 },
                            node_config = self.node_config             ,
                            node_type   = Schema__MGraph__Node         ,
                            value      = "test_node_value"             )
```

## Test Class Structure
Test classes should follow this structure:
1. Helper classes (if needed)
2. setUp method
3. Test methods in logical grouping:
   - Basic initialization tests
   - Type safety validation tests
   - Functionality tests
   - Edge cases/special scenarios

Example:
```python
class Simple_Node(Schema__MGraph__Node): pass                                   # Helper class for testing

class test_Schema__MGraph__Node(TestCase):
    
    def setUp(self):                                                            # Initialize test data
        ...

    def test_init(self):                                                        # Tests basic initialization
        ...

    def test_type_safety_validation(self):                                      # Tests type safety
        ...

    def test_different_value_types(self):                                       # Tests various scenarios
        ...
```

## Comments and Documentation
- Inline documentation should be minimal and descriptive
- Comments explaining test cases should be aligned with the code
- Complex test setups should include explanatory comments

## Additional Guidelines
- Maximum line length should be reasonable (around 120 characters)
- Group related tests together
- Use consistent spacing between methods (one line)
- Maintain alphabetical ordering of imports when possible
- Use clear and descriptive test method names

This specification aims to enhance code readability while maintaining consistent formatting across the codebase.