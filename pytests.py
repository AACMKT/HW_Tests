import main
import random


def test_get_doc_shelf(monkeypatch):
    for i in main.documents:
        doc_num = i['number']
        monkeypatch.setattr('builtins.input', lambda _: doc_num)
        shelf_num = None
        for k, v in main.directories.items():
            if doc_num in v:
                shelf_num = k

        res = main.get_doc_shelf()
        assert res == shelf_num


def test_move_doc_to_shelf(monkeypatch):
    test_doc = '{}-{}-{}'.format(str(random.randrange(100, 999)),
                                 str(random.randrange(100, 999)), str(random.randrange(100, 999)))

    shelves = list(main.directories.keys())
    origin_shelf = str(random.choice(shelves))
    main.directories[origin_shelf].append(test_doc)
    vacant_shelves = shelves.copy()
    vacant_shelves.remove(origin_shelf)
    target_shelf = str(random.choice(vacant_shelves))

    assert test_doc in main.directories[origin_shelf]
    variables = iter([test_doc, target_shelf])
    monkeypatch.setattr('builtins.input', lambda _: next(variables))
    main.move_doc_to_shelf()
    assert test_doc in main.directories[target_shelf]
    assert test_doc not in main.directories[origin_shelf]
    main.directories[target_shelf].remove(test_doc)
