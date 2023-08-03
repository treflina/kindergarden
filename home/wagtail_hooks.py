"""Richtext hooks."""
from django.utils.html import format_html
from django.templatetags.static import static

import wagtail.admin.rich_text.editors.draftail.features as draftail_features
from wagtail import hooks
from wagtail.admin.rich_text.converters.html_to_contentstate import (
    InlineStyleElementHandler,
)


@hooks.register("insert_global_admin_css", order=100)
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static("css/mywagtail.css"))


@hooks.register("register_icons")
def register_icons(icons):
    """Creates additional icons to use in editor's interface and templates"""
    return icons + [
        "home/align-center.svg",
        "home/align-right.svg",
        "home/square-blue.svg",
        "home/square-green.svg",
        "home/square-red.svg",
        "home/square-violet.svg",
        "home/square-violetlight.svg",
    ]


@hooks.register("register_rich_text_features")
def register_centertext_feature(features):
    """Creates centered text in the richtext editor and page."""

    feature_name = "center"
    type_ = "CENTERTEXT"
    tag = "div"

    control = {
        "type": type_,
        "icon": "text-centered",
        "description": "Wyśrodkuj",
        "style": {
            "display": "block",
            "text-align": "center",
        },
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {"element": tag, "props": {"class": "d-block text-center"}}
            }
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_alignright_feature(features):
    """Creates centered text in the richtext editor and page."""

    feature_name = "right"
    type_ = "ALIGNRIGHTTEXT"
    tag = "div"

    control = {
        "type": type_,
        "icon": "align-right",
        "description": "Do prawej",
        "style": {
            "display": "block",
            "text-align": "right",
        },
    }

    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {tag: InlineStyleElementHandler(type_)},
        "to_database_format": {
            "style_map": {
                type_: {"element": tag, "props": {"class": "d-block text-right"}}
            }
        },
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)

    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_smallcaption_feature(features):
    """
    Change slected text color to red
    """
    feature_name = "text-red"
    type_ = "TEXTRED"
    control = {
        "type": type_,
        "icon": "square-red",
        "description": "Czerwony",
        "style": {"color": "red"},
    }
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {
            'span[class="text-red"]': InlineStyleElementHandler(type_)
        },
        "to_database_format": {"style_map": {type_: 'span class="text-red"'}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_smallcaption_feature(features):
    """
    Change selected text color to green
    """
    feature_name = "text-green"
    type_ = "TEXTGREEN"
    control = {
        "type": type_,
        "icon": "square-green",
        "description": "Zielony",
        "style": {"color": "rgb(0, 112, 60)"},
    }
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {
            'span[class="text-red"]': InlineStyleElementHandler(type_)
        },
        "to_database_format": {"style_map": {type_: 'span class="text-green"'}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_smallcaption_feature(features):
    """
    Change selected text color to blue
    """
    feature_name = "text-blue"
    type_ = "TEXTBLUE"
    control = {
        "type": type_,
        "icon": "square-blue",
        "description": "Niebieski",
        "style": {"color": "royalblue"},
    }
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {
            'span[class="text-red"]': InlineStyleElementHandler(type_)
        },
        "to_database_format": {"style_map": {type_: 'span class="text-blue"'}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_smallcaption_feature(features):
    """
    Change selected text color to violet
    """
    feature_name = "text-violet"
    type_ = "TEXTVIOLET"
    control = {
        "type": type_,
        "icon": "square-violet",
        "description": "Fioletowy",
        "style": {"color": "rgb(70,70,157)"},
    }
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {
            'span[class="text-red"]': InlineStyleElementHandler(type_)
        },
        "to_database_format": {"style_map": {type_: 'span class="text-violet"'}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)


@hooks.register("register_rich_text_features")
def register_smallcaption_feature(features):
    """
    Change selected text color to violetlight
    """
    feature_name = "text-violetlight"
    type_ = "TEXTVIOLETLIGHT"
    control = {
        "type": type_,
        "icon": "square-violetlight",
        "description": "Fioletowy jasny",
        "style": {"color": "#993399"},
    }
    features.register_editor_plugin(
        "draftail", feature_name, draftail_features.InlineStyleFeature(control)
    )

    db_conversion = {
        "from_database_format": {
            'span[class="text-red"]': InlineStyleElementHandler(type_)
        },
        "to_database_format": {"style_map": {type_: 'span class="text-violetlight"'}},
    }

    features.register_converter_rule("contentstate", feature_name, db_conversion)
    features.default_features.append(feature_name)
