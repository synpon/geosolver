"""
Sanity check for ontology definitions.
Ensures several things:
1. each type/symbol has only valid keys, and all mandatory keys, and no duplicate definitions of keys
2. no two type/symbol has same name
3. supertype of each type is predefined in types
4. arg_types and return_type of each symbol are defined in types
"""
import logging

__author__ = 'minjoon'


def sanity_check(types, symbols):
    if _sanity_check(types, symbols):
        logging.info("Syntax verification of ontology definitions completed with no error.")
    else:
        raise Exception("Ontology definitions are invalid; see logging.")


def _sanity_check(types, symbols):

    type_mandatory_keys = {'name'}
    type_optional_keys = {'supertype', 'label'}
    type_keys = type_mandatory_keys.union(type_optional_keys)

    symbol_mandatory_keys = {'name', 'arg_types', 'return_type', 'lemma'}
    symbol_optional_keys = ['label']
    symbol_keys = symbol_mandatory_keys.union(symbol_optional_keys)

    type_names = set()
    for idx, type_ in enumerate(types):
        keys = set()
        for key in type_:
            if key not in type_keys:
                logging.error("Invalid key encountered: '%s' at types:%d" % (key, idx))
                return False
            if key in keys:
                logging.error("Duplicate keys encountered: '%s' at types:%d" % (key, idx))
                return False
            keys.add(key)
        if not type_mandatory_keys.issubset(keys):
            missing_keys = type_mandatory_keys.difference(keys)
            logging.error("Some mandatory keys are missing: %r at types:%d" % (missing_keys, idx))
            return False
        if type_['name'] in type_names:
            logging.error("Non-unique name encountered: '%s' at types:%d" % (type_['name'], idx))
            return False
        if 'supertype' in type_ and type_['supertype'] not in type_names:
            logging.error("Unknown 'supertype': '%s' at type %r" % (type_['supertype'], type_))
        type_names.add(type_['name'])

    symbol_names = set()
    for idx, symbol_ in enumerate(symbols):
        keys = set()
        for key in symbol_:
            if key not in symbol_keys:
                logging.error("Invalid key encountered: '%s' at symbols:%d" % (key, idx))
                return False
            if key in keys:
                logging.error("Duplicate keys encountered: '%s' at symbols:%d" % (key, idx))
                return False
            keys.add(key)
        if not symbol_mandatory_keys.issubset(keys):
            missing_keys = symbol_mandatory_keys.difference(keys)
            logging.error("Some mandatory keys are missing: %r at symbol %r" % (list(missing_keys), symbol_))
            return False
        if symbol_['name'] in symbol_names:
            logging.error("Non-unique name encountered: '%s' at symbol %r" % (symbol_['name'], symbol_))
            return False
        for arg_type in symbol_['arg_types']:
            if arg_type not in type_names:
                logging.error("Unknown arg type: '%s' at symbol %r" % (arg_type, symbol_))
                return False
        if symbol_['return_type'] not in type_names:
            logging.error("Unknown return type: '%s' at symbol %r" % (symbol_['return_type'], symbol_))
            return False

        symbol_names.add(symbol_['name'])

    # passed every test
    return True

