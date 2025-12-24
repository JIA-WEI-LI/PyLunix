ToggleButton
============

.. tab-set::

   .. tab-item:: ToggleButton
      :sync: base

      .. currentmodule:: pylunix.components.controls.toggle_button.toggle_button

      Example Code

      .. literalinclude:: ../../examples/basic_inputs/togglebutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      .. attention::
         **Visual Contrast & Transparency**

         The **Default** theme utilizes white color combined with **alpha channels (transparency)** to achieve its visual effects.

         * **Dark Background (Recommended):** On a dark background (e.g., ``#222222``), the semi-transparent layers blend to create distinct gray scales and hover highlights.
         * **Light Background Warning:** If used on a light or white background, these effects will become invisible as white-on-white contrast is nearly zero. Dynamic states like **Hover** or **Pressed** will appear non-responsive.

         **Recommendation:** Always ensure the parent container provides sufficient contrast when using transparency-based themes.

      API Reference

      .. autoclass:: ToggleButton
         :members:
         :exclude-members: paintEvent
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: TransparentToggleButton
      :sync: transparenttoggle

      .. currentmodule:: pylunix.components.controls.toggle_button.toggle_button

      Example Code

      .. literalinclude:: ../../examples/basic_inputs/transparenttogglebutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      API Reference

      .. autoclass:: TransparentToggleButton
         :members:
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: SegmentedButton
      :sync: segmented

      .. currentmodule:: pylunix.components.controls.toggle_button.toggle_button

      API Reference 

      .. autoclass:: SegmentedButton
         :members:
         :show-inheritance:
         :special-members: __init__