ToolButton
==========

A collection of specialized tool buttons featuring dynamic SVG coloring, state-aware opacity, and flexible icon-text alignment.

.. tab-set::

   .. tab-item:: ToolButton
      :sync: tool

      .. currentmodule:: pylunix.components.controls.tool_button.tool_button

      The base tool button class. It manually renders icons and text to ensure theme-consistent coloring and precise centering.

      Example Code
      
      .. literalinclude:: ../../examples/basic_inputs/toolbutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      .. attention::
         **Visual Contrast & Transparency**

         The **Default** theme utilizes white color combined with **alpha channels (transparency)** to achieve its visual effects.

         * **Dark Background (Recommended):** On a dark background (e.g., ``#222222``), the semi-transparent layers blend to create distinct gray scales and hover highlights.
         * **Light Background Warning:** If used on a light or white background, these effects will become invisible.

      API Reference

      .. autoclass:: ToolButton
         :members:
         :exclude-members: paintEvent, mousePressEvent, mouseReleaseEvent, enterEvent, leaveEvent
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: PrimaryToolButton
      :sync: primary_tool

      .. currentmodule:: pylunix.components.controls.tool_button.tool_button

      A tool button that uses the system's **Accent/Primary** color for its foreground (icon and text), making it stand out as a key action.

      Example Code
      
      .. literalinclude:: ../../examples/basic_inputs/primary_toolbutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      API Reference

      .. autoclass:: PrimaryToolButton
         :members:
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: ToggleToolButton
      :sync: toggle_tool

      .. currentmodule:: pylunix.components.controls.tool_button.tool_button

      A checkable tool button that switches between **On** and **Off** states, supporting independent icons for each state.

      Example Code
      
      .. literalinclude:: ../../examples/basic_inputs/toggle_toolbutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      API Reference 

      .. autoclass:: ToggleToolButton
         :members:
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: Transparent Variants
      :sync: transparent_tool

      .. currentmodule:: pylunix.components.controls.tool_button.tool_button

      Lightweight variants with transparent backgrounds in idle state, including both standard and toggle versions.

      * **TransparentToolButton**: Standard behavior with ghost styling.
      * **TransparentToggleToolButton**: Toggle behavior with ghost styling.

      Example Code
      
      .. literalinclude:: ../../examples/basic_inputs/transparent_toolbutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      API Reference

      .. autoclass:: TransparentToolButton
         :members:
         :show-inheritance:
         :special-members: __init__

      .. autoclass:: TransparentToggleToolButton
         :members:
         :show-inheritance:
         :special-members: __init__