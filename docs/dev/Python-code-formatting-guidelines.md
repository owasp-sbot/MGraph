# Python Code Formatting Guidelines


# Code Formatting Philosophy, Principles and Specification

## Core Principles

### 1. Visual Pattern Recognition
The human brain excels at pattern recognition. This formatting prioritizes creating clear visual patterns that make code structure immediately apparent: 
- Aligned equals signs create vertical lanes that guide the eye
- Consistent comma placement creates predictable rhythm
- Grouped imports with aligned elements form distinct visual blocks

### 2. Information Density vs Readability
While PEP-8 often spreads code across many lines for "readability", this approach recognizes that excessive vertical spread can actually harm comprehension by:

- Forcing more scrolling
- Breaking mental context
- Making patterns harder to spot
- Reducing the amount of code visible at once

### 3. Contextual Proximity
Related information should be visually close to enhance understanding:
- Method documentation appears on the same line as the method definition
- Constructor parameters align vertically to show relationships
- Dictionary key-value pairs maintain close horizontal proximity

## Departures from PEP-8

### Why We Differ

PEP-8's formatting guidelines, while well-intentioned, can create several practical issues:

1. Vertical Space Inefficiency
```python
# PEP-8 style
self.method_call(
    parameter_one="value",
    parameter_two="value",
    parameter_three="value"
)

# This style
self.method_call(parameter_one   = "value",
                parameter_two   = "value",
                parameter_three = "value")
```

2. Loss of Visual Patterns
```python
# PEP-8 style
assert something.value == expected_value
assert something_else.other_value == other_expected_value
assert third_thing.final_value == final_expected_value

# This style
assert something.value          == expected_value
assert something_else.value     == other_expected_value
assert third_thing.final_value  == final_expected_value
```

3. Broken Visual Context
```python
# PEP-8 style - related elements separated
class SomeClass:
    
    def __init__(
        self,
        param_one,
        param_two
    ):
        self.param_one = param_one
        self.param_two = param_two

# This style - related elements together
class SomeClass:
    def __init__(self, param_one,
                      param_two ):
        self.param_one = param_one
        self.param_two = param_two
```

## Benefits of Our Approach

1. Enhanced Scanning
- Column alignment makes it easy to scan for specific elements
- Consistent patterns reduce cognitive load
- Related information stays visually grouped

2. Better Maintainability
- Alignment makes inconsistencies immediately visible
- Format violations stand out visually
- Pattern adherence encourages consistent updates

3. Improved Debugging
- Clear visual structure helps spot logical errors
- Aligned comparisons make value mismatches obvious
- Grouped information reduces context switching

4. Code Review Efficiency
- Structured patterns make changes more apparent
- Consistent formatting reduces noise in diffs
- Visual grouping helps reviewers understand intent

## Real-World Impact

This formatting approach has proven particularly valuable in:
- Large codebases where pattern recognition becomes crucial
- Test files where structure and relationships matter more than PEP-8 conformity
- Code review processes where visual clarity speeds up reviews
- Debugging sessions where quick scanning and pattern recognition are essential

Our philosophy prioritizes human factors and practical utility over strict adherence to style guidelines, recognizing that code is read far more often than it is written.


# Python Code Formatting Specification

## Import Statements
Imports should be aligned with the longest import path, using spaces between major groups:

```python
from unittest                                        import TestCase
from mgraph_ai.schemas.Schema__MGraph__Node          import Schema__MGraph__Node
from mgraph_ai.schemas.Schema__MGraph__Node__Config  import Schema__MGraph__Node__Config
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
```

## Constructor Calls
Constructor calls should be formatted with aligned parameters, aligned equals signs, and aligned commas:

```python
node_config = Schema__MGraph__Node__Config(node_id    = Random_Guid(),
                                           value_type = str          )

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
assert type(self.node) is Schema__MGraph__Node
assert self.node.node_data == self.node_data
assert self.node.value == "test_node_value"
assert len(self.node.attributes) == 1
assert self.node.attributes[self.attribute.attribute_id] == self.attribute
```

## Dictionary Literals
Dictionary literals in constructor calls should maintain alignment while using minimal line breaks:

```python
node = Schema__MGraph__Node(attributes={attr_1.attribute_id: attr_1,
                                        attr_2.attribute_id: attr_2},
                            node_config=self.node_data,
                            node_type=Schema__MGraph__Node,
                            value="test_node_value")
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