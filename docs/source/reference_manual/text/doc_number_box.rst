NumberBox [Experimental]
========================

.. currentmodule:: pylunix.components.controls.number_box.number_box

.. warning::

   .. versionadded:: 0.2.0-alpha2

   **Experimental Feature**: The ``NumberBox`` component is currently in active development. 
   API breaking changes may occur in future releases without prior notice.

.. admonition:: Under Development
   :class: note
   
   The following features are currently under development and may not function as expected:

   * **Value Adjustment Buttons**: Interactive buttons (e.g., +/-) for incrementally adjusting numeric values.
   * **Decimal Formatting**: Automatic conversion and rounding of decimal places after numeric input.

Example Code

.. literalinclude:: ../../examples/text/number_box_example.py
    :language: python
    :caption: example.py
    :linenos:

API Reference

.. autoclass:: NumberBox
    :members:
    :exclude-members: paintEvent, valueChanged
    :show-inheritance:
    :special-members: __init__