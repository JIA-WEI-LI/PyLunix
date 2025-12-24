Button
======

.. tab-set::

   .. tab-item:: BaseButton
      :sync: base

      .. currentmodule:: pylunix.components.controls.button.button

      API Reference

      .. autoclass:: BaseButton
         :members:
         :exclude-members: paintEvent
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: PushButton
      :sync: push

      .. currentmodule:: pylunix.components.controls.button.button

      Example Code
      
      .. literalinclude:: ../../examples/basic_inputs/pushbutton_example.py
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

      .. autoclass:: PushButton
         :members:
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: PrimaryButton
      :sync: primary

      .. currentmodule:: pylunix.components.controls.button.button

      Example Code
      
      .. literalinclude:: ../../examples/basic_inputs/primarybutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      API Reference 

      .. autoclass:: PrimaryButton
         :members:
         :show-inheritance:
         :special-members: __init__

   .. tab-item:: TransparentPushButton
      :sync: transparent

      .. currentmodule:: pylunix.components.controls.button.button

      Example Code
      
      .. literalinclude:: ../../examples/basic_inputs/transparentpushbutton_example.py
         :language: python
         :caption: example.py
         :linenos:

      API Reference

      .. autoclass:: TransparentPushButton
         :members:
         :show-inheritance:
         :special-members: __init__