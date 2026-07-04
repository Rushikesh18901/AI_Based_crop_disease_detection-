# Translator utility for multi-language support
# Uses local dictionary for reliable translations

TRANSLATIONS = {
    "English": {},
    "Hindi": {
        "Upload a crop leaf image": "पत्ती की छवि अपलोड करें",
        "Low confidence — try a clearer image.": "कम भरोसा। स्पष्ट छवि अपलोड करें",
        "Tank Size (Litres)": "टैंक आकार (लीटर)",
        "Set Spray Reminder": "स्प्रे रिमाइंडर सेट करें",
        "Reminder saved successfully!": "रिमाइंडर सहेजा गया!",
        "No history available yet.": "अभी तक कोई इतिहास उपलब्ध नहीं",
        "Plant": "पौधा",
        "Disease": "रोग",
        "Detection score": "पहचान स्कोर",
        "Confidence": "विश्वास",
        "Crop Health Analysis": "फसल स्वास्थ्य विश्लेषण",
        "Pesticide Recommendation": "कीटनाशक सिफारिश",
        "Recommended": "अनुशंसित",
        "Dosage per Litre": "प्रति लीटर खुराक",
        "Spray Interval": "स्प्रे अंतराल",
        "Dosage Calculator": "खुराक कैलकुलेटर",
        "Fertilizer Recommendation": "उर्वरक सिफारिश",
        "Fertilizer": "उर्वरक",
        "Usage": "उपयोग",
        "Frequency": "आवृत्ति",
        "Safety Instructions": "सुरक्षा निर्देश",
        "Next Spray Schedule": "अगला स्प्रे शेड्यूल",
        "Next Spray Date": "अगली स्प्रे तिथि",
        "Days Remaining": "शेष दिन",
        "Scan Leaf": "पत्ती स्कैन करें",
        "Detection Result": "पहचान परिणाम",
        "Crop Health": "फसल स्वास्थ्य",
        "Health Score": "स्वास्थ्य स्कोर",
        "Yield Loss": "उपज हानि",
        "For": "के लिए",
        "Per Litre": "प्रति लीटर",
    },
    "Marathi": {
        "Upload a crop leaf image": "पानाची प्रतिमा अपलोड करा",
        "Low confidence — try a clearer image.": "कम विश्वास. स्पष्ट प्रतिमा घ्या.",
        "Tank Size (Litres)": "टाकीचा आकार (लीटर)",
        "Set Spray Reminder": "स्प्रे रिमाइंडर सेट करा",
        "Reminder saved successfully!": "रिमाइंडर सेव केले!",
        "No history available yet.": "इतिहास उपलब्ध नाही",
        "Plant": "वनस्पती",
        "Disease": "रोग",
        "Detection score": "शोध स्कोर",
        "Confidence": "विश्वास",
        "Crop Health Analysis": "पिकाचे आरोग्य विश्लेषण",
        "Pesticide Recommendation": "कीटकाशक शिफारस",
        "Recommended": "शिफारस केलेले",
        "Dosage per Litre": "प्रति लीटर डोस",
        "Spray Interval": "स्प्रे अंतराल",
        "Dosage Calculator": "डोस कॅलक्युलेटर",
        "Fertilizer Recommendation": "खत शिफारस",
        "Fertilizer": "खत",
        "Usage": "वापर",
        "Frequency": "वारंवारता",
        "Safety Instructions": "सुरक्षा सूचना",
        "Next Spray Schedule": "पुढील स्प्रे शेड्यूल",
        "Next Spray Date": "पुढील स्प्रे तारीख",
        "Days Remaining": "उर्वरित दिवस",
        "Scan Leaf": "पान स्कैन करा",
        "Detection Result": "शोध निकाल",
        "Crop Health": "पिकाचे आरोग्य",
        "Health Score": "आरोग्य स्कोर",
        "Yield Loss": "उत्पादन हानी",
        "For": "साठी",
        "Per Litre": "प्रति लीटर",
    },
}


def translate_text(text, language):
    if language == "English":
        return text

    lang_key = language.capitalize()
    if lang_key in TRANSLATIONS and text in TRANSLATIONS[lang_key]:
        return TRANSLATIONS[lang_key][text]

    for key in TRANSLATIONS:
        if key.lower() == lang_key.lower():
            if text in TRANSLATIONS[key]:
                return TRANSLATIONS[key][text]
            break

    return text
