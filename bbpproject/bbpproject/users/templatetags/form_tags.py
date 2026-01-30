from django import template

register = template.Library()


@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Add CSS classes to a form field's widget.

    Usage: {{ form.email|add_class:"border-2 focus:ring-2" }}

    This filter is defensive: if `field` is already a rendered string
    (or anything without `as_widget`), it returns it unchanged. If the
    widget already has a `class` attribute it will be merged.
    """
    # If the object is a BoundField (has as_widget), render with merged attrs.
    if hasattr(field, "as_widget"):
        # Try to get any existing classes from the underlying widget attrs.
        existing = ""
        try:
            existing = getattr(field, "field", None)
            if existing is not None:
                existing = existing.widget.attrs.get("class", "")
            else:
                existing = ""
        except Exception:
            existing = ""

        combined = " ".join(filter(None, [existing.strip(), css_class.strip()]))
        attrs = {"class": combined} if combined else {}
        return field.as_widget(attrs=attrs)

    # If it's not a BoundField (e.g. already a string), just return it.
    return field
