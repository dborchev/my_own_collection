#!/usr/bin/python

# Copyright: (c) 2022, Denis Borchev <dborchev@example.org>
# MIT License
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type
import os


DOCUMENTATION = r'''
---
module: my_own_module

short_description: Stores content to text file at path on the host

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: Stores the "content" to a text file at "path" on the host

options:
    content:
        description: The content of the target file
        required: true
        type: str
    path:
        description: The path to the target file
        required: true
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - dborchev.my_collection.my_doc_fragment_name

author:
    - Denis Borchev (@dborchev)
'''

EXAMPLES = r'''
# Create a file
- name: Create file
  dborchev.my_collection.my_own_module:
    content: "hello world"
    path: "/tmp/test_my_own_module"
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
is_ok:
    description: we are ok
    type: bool
    returned: always
    sample: True
'''

from ansible.module_utils.basic import AnsibleModule


def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        content=dict(type='str', required=True),
        path=dict(type='str', required=True)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        changed=False,
        is_ok=False,
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if not os.path.exists(module.params.get('path')):
        result['changed'] = True
    else:
        # check if the contents of the file are as we expect them:
        with open(module.params['path'], 'r') as f:
            data = file.read()
        result['changed'] = not data == module.params.get('content')

    if module.check_mode:
        module.exit_json(**result)

    with open(module.params['path'], 'w+') as f:
        f.write(module.params.get('content'))
        result['is_ok'] = True

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

