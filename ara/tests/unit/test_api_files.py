#  Copyright (c) 2017 Red Hat, Inc.
#
#  This file is part of ARA: Ansible Run Analysis.
#
#  ARA is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  ARA is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with ARA.  If not, see <http://www.gnu.org/licenses/>.

from ara.tests.unit.common import ansible_run
from ara.tests.unit.common import TestAra
from ara.api.files import FileApi
import ara.db.models as models

from oslo_serialization import jsonutils


class TestApiFiles(TestAra):
    """ Tests for the ARA API interface """
    def setUp(self):
        super(TestApiFiles, self).setUp()

    def tearDown(self):
        super(TestApiFiles, self).tearDown()

    ###########
    # POST
    ###########
    # Not implemented yet
    def test_post_http_unimplemented(self):
        res = self.client.post('/api/v1/files')
        self.assertEqual(res.status_code, 405)

    def test_post_internal_unimplemented(self):
        res = FileApi().post()
        self.assertEqual(res.status_code, 405)

    def test_post_equivalence(self):
        http = self.client.post('/api/v1/files')
        internal = FileApi().post()
        self.assertEqual(http.status_code, internal.status_code)
        self.assertEqual(http.data, internal.data)

    ###########
    # PUT
    ###########
    # Not implemented yet
    def test_put_http_unimplemented(self):
        res = self.client.put('/api/v1/files')
        self.assertEqual(res.status_code, 405)

    def test_put_internal_unimplemented(self):
        res = FileApi().put()
        self.assertEqual(res.status_code, 405)

    def test_put_equivalence(self):
        http = self.client.put('/api/v1/files')
        internal = FileApi().put()
        self.assertEqual(http.status_code, internal.status_code)
        self.assertEqual(http.data, internal.data)

    ###########
    # DELETE
    ###########
    # Not implemented yet
    def test_delete_http_unimplemented(self):
        res = self.client.delete('/api/v1/files')
        self.assertEqual(res.status_code, 405)

    def test_delete_internal_unimplemented(self):
        res = FileApi().delete()
        self.assertEqual(res.status_code, 405)

    def test_delete_equivalence(self):
        http = self.client.delete('/api/v1/files')
        internal = FileApi().delete()
        self.assertEqual(http.status_code, internal.status_code)
        self.assertEqual(http.data, internal.data)

    ###########
    # GET
    ###########
    def test_get_http_help(self):
        res = self.client.get('/api/v1/files',
                              query_string=dict(help=True))
        self.assertEqual(res.status_code, 200)
        # TODO: Improve this
        self.assertTrue(b'result_output' in res.data)
        self.assertTrue(b'query_parameters' in res.data)

    def test_get_http_without_parameters_and_data(self):
        res = self.client.get('/api/v1/files')
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"[]\n")

    def test_get_internal_without_parameters_and_data(self):
        res = FileApi().get()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.data, b"[]\n")

    def test_get_equivalence_without_parameters_and_data(self):
        http = self.client.get('/api/v1/files')
        internal = FileApi().get()
        self.assertEqual(http.status_code, internal.status_code)
        self.assertEqual(http.data, internal.data)

    def test_get_http_without_parameters(self):
        ctx = ansible_run()
        res = self.client.get('/api/v1/files')
        self.assertEqual(res.status_code, 200)

        data = jsonutils.loads(res.data)[1]

        self.assertEqual(ctx['playbook'].file.id,
                         data['id'])
        self.assertEqual(ctx['playbook'].file.playbook_id,
                         data['playbook_id'])
        self.assertEqual(ctx['playbook'].file.path,
                         data['path'])
        self.assertEqual(ctx['playbook'].file.is_playbook,
                         data['is_playbook'])

    def test_get_internal_without_parameters(self):
        ctx = ansible_run()
        res = FileApi().get()
        self.assertEqual(res.status_code, 200)

        data = jsonutils.loads(res.data)[1]

        self.assertEqual(ctx['playbook'].file.id,
                         data['id'])
        self.assertEqual(ctx['playbook'].file.playbook_id,
                         data['playbook_id'])
        self.assertEqual(ctx['playbook'].file.path,
                         data['path'])
        self.assertEqual(ctx['playbook'].file.is_playbook,
                         data['is_playbook'])

    def test_get_equivalence_without_parameters(self):
        ansible_run()
        http = self.client.get('/api/v1/files')
        internal = FileApi().get()
        self.assertEqual(http.status_code, internal.status_code)
        self.assertEqual(http.data, internal.data)

    def test_get_http_with_id(self):
        ctx = ansible_run()
        files = models.File.query.all()
        self.assertEqual(len(files), 2)

        res = self.client.get('/api/v1/files', query_string=dict(id=1))
        self.assertEqual(res.status_code, 200)

        data = jsonutils.loads(res.data)
        # Ensure we only get the one play we want back
        self.assertEqual(len(data), 1)
        self.assertEqual(ctx['playbook'].file.id, 1)

        data = data[0]
        self.assertEqual(ctx['playbook'].file.id,
                         data['id'])
        self.assertEqual(ctx['playbook'].file.playbook_id,
                         data['playbook_id'])
        self.assertEqual(ctx['playbook'].file.path,
                         data['path'])
        self.assertEqual(ctx['playbook'].file.is_playbook,
                         data['is_playbook'])

    def test_get_internal_with_id(self):
        ctx = ansible_run()
        files = models.File.query.all()
        self.assertEqual(len(files), 2)

        res = FileApi().get(id=1)
        self.assertEqual(res.status_code, 200)

        data = jsonutils.loads(res.data)
        # Ensure we only get the one playbook we want back
        self.assertEqual(len(data), 1)
        self.assertEqual(ctx['playbook'].file.id, 1)

        data = data[0]
        self.assertEqual(ctx['playbook'].file.id,
                         data['id'])
        self.assertEqual(ctx['playbook'].file.playbook_id,
                         data['playbook_id'])
        self.assertEqual(ctx['playbook'].file.path,
                         data['path'])
        self.assertEqual(ctx['playbook'].file.is_playbook,
                         data['is_playbook'])

    def test_get_equivalence_with_id(self):
        ansible_run()
        files = models.File.query.all()
        self.assertEqual(len(files), 2)

        http = self.client.get('/api/v1/files', query_string=dict(id=1))
        internal = FileApi().get(id=1)
        self.assertEqual(http.status_code, internal.status_code)
        self.assertEqual(http.data, internal.data)
