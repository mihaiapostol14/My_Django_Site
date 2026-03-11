class FieldExtractorMixin:
    def get_form_fields(self, form_class):
        """
       A universal field extractor for any Django form.
       Used for quickly copying field names to views.py.
        """
        if hasattr(form_class, 'base_fields'):
            fields_list = list(form_class.base_fields.keys())
            print("\n" + "=" * 40)
            print(f"FORM STRUCTURE: {form_class.__name__}")
            print("COPY THIS LIST OF FIELDS:")
            print(fields_list)
            print("=" * 40 + "\n")
            return fields_list
        else:
            print("Error: The passed object is not a Django form class.")
            return []
