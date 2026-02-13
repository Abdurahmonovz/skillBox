# course_content.py

COURSE = {
    "title": "Python Kurslari",
    "modules": [
        {
            "id": 1,
            "title": "1. IDE o‘rnatish va sozlash",
            "lessons": [
                {
                    "id": 1,
                    "title": "1.1 PyCharm o‘rnatish",
                    "desc": "PyCharm o‘rnatish va dastlabki sozlash.",
                    "video": "VIDEO_FILE_ID_1_1",
                    "pdfs": ["PDF_FILE_ID_1_A", "PDF_FILE_ID_1_B"],
                },
                {
                    "id": 2,
                    "title": "1.2 VS Code sozlash",
                    "desc": "VS Code, extensions va Python interpreter.",
                    "video": "VIDEO_FILE_ID_1_2",
                    "pdfs": [],
                },
                # ... 6 ta bo‘lsin
            ],
        },
        {
            "id": 2,
            "title": "2. Tayanch to‘plamlar: ro‘yxatlar",
            "lessons": [
                {"id": 1, "title": "2.1 List kirish", "desc": "List nima?", "video": "VIDEO_FILE_ID_2_1", "pdfs": ["PDF_FILE_ID_2"]},
                {"id": 2, "title": "2.2 Index va slice", "desc": "Index/slice", "video": "VIDEO_FILE_ID_2_2", "pdfs": []},
                {"id": 3, "title": "2.3 Add/Remove", "desc": "append/pop/remove", "video": "VIDEO_FILE_ID_2_3", "pdfs": []},
                {"id": 4, "title": "2.4 Amaliy", "desc": "Mashqlar", "video": "VIDEO_FILE_ID_2_4", "pdfs": []},
            ],
        },

        # 3-modul (4 video + 1 pdf)
        {"id": 3, "title": "3. Ro‘yxatlar bilan ishlash usullari", "lessons": [
            {"id": 1, "title": "3.1 sort/reverse", "desc": "Tartiblash", "video": "VIDEO_FILE_ID_3_1", "pdfs": ["PDF_FILE_ID_3"]},
            {"id": 2, "title": "3.2 copy/clear", "desc": "Nusxa olish", "video": "VIDEO_FILE_ID_3_2", "pdfs": []},
            {"id": 3, "title": "3.3 join/split", "desc": "Matn bilan", "video": "VIDEO_FILE_ID_3_3", "pdfs": []},
            {"id": 4, "title": "3.4 Amaliy", "desc": "Mashqlar", "video": "VIDEO_FILE_ID_3_4", "pdfs": []},
        ]},

        # 4-modul (6 video + 1 pdf)
        {"id": 4, "title": "4. List comprehensions", "lessons": [
            {"id": 1, "title": "4.1 Kirish", "desc": "Sintaksis", "video": "VIDEO_FILE_ID_4_1", "pdfs": ["PDF_FILE_ID_4"]},
            {"id": 2, "title": "4.2 if bilan", "desc": "Filter", "video": "VIDEO_FILE_ID_4_2", "pdfs": []},
            {"id": 3, "title": "4.3 nested", "desc": "Ichma-ich", "video": "VIDEO_FILE_ID_4_3", "pdfs": []},
            {"id": 4, "title": "4.4 dict/set", "desc": "Boshqa turlar", "video": "VIDEO_FILE_ID_4_4", "pdfs": []},
            {"id": 5, "title": "4.5 amaliy", "desc": "Mashqlar", "video": "VIDEO_FILE_ID_4_5", "pdfs": []},
            {"id": 6, "title": "4.6 xatolar", "desc": "Eng ko‘p xatolar", "video": "VIDEO_FILE_ID_4_6", "pdfs": []},
        ]},

        # 5-modul (5 video + 1 pdf)
        {"id": 5, "title": "5. Asosiy to‘plamlar: setlar", "lessons": [
            {"id": 1, "title": "5.1 set kirish", "desc": "Set nima?", "video": "VIDEO_FILE_ID_5_1", "pdfs": ["PDF_FILE_ID_5"]},
            {"id": 2, "title": "5.2 add/remove", "desc": "Metodlar", "video": "VIDEO_FILE_ID_5_2", "pdfs": []},
            {"id": 3, "title": "5.3 union/intersection", "desc": "Amallar", "video": "VIDEO_FILE_ID_5_3", "pdfs": []},
            {"id": 4, "title": "5.4 difference", "desc": "Farqlar", "video": "VIDEO_FILE_ID_5_4", "pdfs": []},
            {"id": 5, "title": "5.5 amaliy", "desc": "Mashqlar", "video": "VIDEO_FILE_ID_5_5", "pdfs": []},
        ]},

        # 6-modul (5 video + 1 pdf)
        {"id": 6, "title": "6. Lug‘atlar va kolleksiyalar", "lessons": [
            {"id": 1, "title": "6.1 dict kirish", "desc": "dict nima?", "video": "VIDEO_FILE_ID_6_1", "pdfs": ["PDF_FILE_ID_6"]},
            {"id": 2, "title": "6.2 get/keys/values", "desc": "Metodlar", "video": "VIDEO_FILE_ID_6_2", "pdfs": []},
            {"id": 3, "title": "6.3 items loop", "desc": "Loop", "video": "VIDEO_FILE_ID_6_3", "pdfs": []},
            {"id": 4, "title": "6.4 nested", "desc": "Ichma-ich dict", "video": "VIDEO_FILE_ID_6_4", "pdfs": []},
            {"id": 5, "title": "6.5 amaliy", "desc": "Mashqlar", "video": "VIDEO_FILE_ID_6_5", "pdfs": []},
        ]},

        # 7-modul (7 video + 1 pdf)
        {"id": 7, "title": "7. Kortejlar", "lessons": [
            {"id": 1, "title": "7.1 tuple kirish", "desc": "tuple nima?", "video": "VIDEO_FILE_ID_7_1", "pdfs": ["PDF_FILE_ID_7"]},
            {"id": 2, "title": "7.2 unpacking", "desc": "unpack", "video": "VIDEO_FILE_ID_7_2", "pdfs": []},
            {"id": 3, "title": "7.3 index/slice", "desc": "slice", "video": "VIDEO_FILE_ID_7_3", "pdfs": []},
            {"id": 4, "title": "7.4 tuple vs list", "desc": "farqi", "video": "VIDEO_FILE_ID_7_4", "pdfs": []},
            {"id": 5, "title": "7.5 amaliy", "desc": "mashqlar", "video": "VIDEO_FILE_ID_7_5", "pdfs": []},
            {"id": 6, "title": "7.6 xatolar", "desc": "xatolar", "video": "VIDEO_FILE_ID_7_6", "pdfs": []},
            {"id": 7, "title": "7.7 yakun", "desc": "yakun", "video": "VIDEO_FILE_ID_7_7", "pdfs": []},
        ]},

        # 8-modul (7 video + 1 pdf)
        {"id": 8, "title": "8. Funksiyalar: davomi", "lessons": [
            {"id": 1, "title": "8.1 args/kwargs", "desc": "args kwargs", "video": "VIDEO_FILE_ID_8_1", "pdfs": ["PDF_FILE_ID_8"]},
            {"id": 2, "title": "8.2 return", "desc": "return", "video": "VIDEO_FILE_ID_8_2", "pdfs": []},
            {"id": 3, "title": "8.3 scope", "desc": "scope", "video": "VIDEO_FILE_ID_8_3", "pdfs": []},
            {"id": 4, "title": "8.4 lambda", "desc": "lambda", "video": "VIDEO_FILE_ID_8_4", "pdfs": []},
            {"id": 5, "title": "8.5 map/filter", "desc": "map filter", "video": "VIDEO_FILE_ID_8_5", "pdfs": []},
            {"id": 6, "title": "8.6 recursion", "desc": "recursion", "video": "VIDEO_FILE_ID_8_6", "pdfs": []},
            {"id": 7, "title": "8.7 amaliy", "desc": "amaliy", "video": "VIDEO_FILE_ID_8_7", "pdfs": []},
        ]},

        # 9-modul (5 video + 1 pdf)
        {"id": 9, "title": "9. Fayllar bilan ishlash", "lessons": [
            {"id": 1, "title": "9.1 open/read", "desc": "read", "video": "VIDEO_FILE_ID_9_1", "pdfs": ["PDF_FILE_ID_9"]},
            {"id": 2, "title": "9.2 write", "desc": "write", "video": "VIDEO_FILE_ID_9_2", "pdfs": []},
            {"id": 3, "title": "9.3 with", "desc": "context", "video": "VIDEO_FILE_ID_9_3", "pdfs": []},
            {"id": 4, "title": "9.4 json", "desc": "json", "video": "VIDEO_FILE_ID_9_4", "pdfs": []},
            {"id": 5, "title": "9.5 amaliy", "desc": "amaliy", "video": "VIDEO_FILE_ID_9_5", "pdfs": []},
        ]},

        # 10-modul (5 video + 1 pdf)
        {"id": 10, "title": "10. Istisnolar: xatolar ustida ishlash", "lessons": [
            {"id": 1, "title": "10.1 try/except", "desc": "try except", "video": "VIDEO_FILE_ID_10_1", "pdfs": ["PDF_FILE_ID_10"]},
            {"id": 2, "title": "10.2 finally", "desc": "finally", "video": "VIDEO_FILE_ID_10_2", "pdfs": []},
            {"id": 3, "title": "10.3 raise", "desc": "raise", "video": "VIDEO_FILE_ID_10_3", "pdfs": []},
            {"id": 4, "title": "10.4 custom errors", "desc": "custom", "video": "VIDEO_FILE_ID_10_4", "pdfs": []},
            {"id": 5, "title": "10.5 amaliy", "desc": "amaliy", "video": "VIDEO_FILE_ID_10_5", "pdfs": []},
        ]},
    ],
}
