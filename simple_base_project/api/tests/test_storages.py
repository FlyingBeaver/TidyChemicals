from random import seed
from api.tests.setup import BasicApiTest, rchoice, rchoice_exclude
from chemicals.models import Chemical, StoragePlace


seed(1)


class RootStorageApiTest(BasicApiTest):
    def test_get_authorized(self):
        self.billie_eilish_logs_in()
        response = self.client.get('/api/v1/root-storage')
        resp_data = response.data
        self.assertEqual(response.status_code, 200)

        root_storage = StoragePlace.objects.get(level=0)
        storage_data = {
            "id": root_storage.id,
            "name": root_storage.name
        }
        self.assertEqual(resp_data, storage_data)

    def test_post_authorized(self):
        self.billie_eilish_logs_in()
        will_be_send = {"id": 1000,
                      "name": "New root storage"}
        response = self.client.post(
            '/api/v1/root-storage',
            will_be_send,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 405)

    def test_put_authorized(self):
        self.billie_eilish_logs_in()
        will_be_send = {"id": 1,
                      "name": "New name"}
        response = self.client.put(
            '/api/v1/root-storage',
            will_be_send,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 405)

    def test_delete_authorized(self):
        self.billie_eilish_logs_in()
        response = self.client.delete('/api/v1/root-storage')
        self.assertEqual(response.status_code, 405)


    def test_unauthorized(self):
        response_get = self.client.get('/api/v1/root-storage')
        self.assertEqual(response_get.status_code, 403)
        
        will_be_send = {"id": 1000,
                      "name": "New root storage"}
        response_post = self.client.post(
            '/api/v1/root-storage',
            will_be_send,
            content_type="application/json"
        )
        self.assertEqual(response_post.status_code, 403)

        will_be_send = {"id": 1,
                      "name": "New name"}
        response_put = self.client.put(
            '/api/v1/root-storage',
            will_be_send,
            content_type="application/json"
        )
        self.assertEqual(response_put.status_code, 403)

        response_delete = self.client.delete('/api/v1/root-storage')
        self.assertEqual(response_delete.status_code, 403)


class StoragesApiTest(BasicApiTest):
    def test_list_authorized(self):
        self.billie_eilish_logs_in()
        response = self.client.get("/api/v1/storages")
        self.assertEqual(response.status_code, 405)

    def test_post_authorized(self):
        self.billie_eilish_logs_in()
        queryset = StoragePlace.objects.all()
        uninitialized = filter(
            lambda x: not x.initialized,
            queryset
        )
        parent_storage = rchoice(uninitialized)
        storage_data = {
            "name": "Supadupastorage",
            "parent": parent_storage.id
        }
        response = self.client.post(
            "/api/v1/storages",
            storage_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        new_storage = StoragePlace.objects.get(
            name="Supadupastorage"
        )
        self.assertEqual(new_storage.parent, parent_storage.id)

    def test_post_authorized_1(self):
        self.billie_eilish_logs_in()
        queryset = StoragePlace.objects.all()
        with_children = filter(
            lambda x: x.has_children,
            queryset
        )
        parent_storage = rchoice(with_children)
        child = rchoice(
            StoragePlace.objects.filter(
                parent=parent_storage.id
            )
        )
        storage_data = {
            "name": child.name,
            "parent": parent_storage.id
        }
        response = self.client.post(
            "/api/v1/storages",
            storage_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_post_authorized_2(self):
        self.billie_eilish_logs_in()
        storage_data = {
            "name": "Supadupastorage",
            "parent": 1000
        }
        response = self.client.post(
            "/api/v1/storages",
            storage_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_post_authorized_3(self):
        self.billie_eilish_logs_in()
        parent_storage = rchoice(StoragePlace.objects.all())
        storage_data = {
            "name": "",
            "parent": parent_storage.id
        }
        response = self.client.post(
            "/api/v1/storages",
            storage_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)

    def test_post_authorized_4(self):
        self.billie_eilish_logs_in()
        storage_data = {
            "name": "Supadupastorage",
            "parent": None
        }
        response = self.client.post(
            "/api/v1/storages",
            storage_data,
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_post_authorized_5(self):
        self.billie_eilish_logs_in()
        parent = rchoice(
            filter(
                lambda x: not x.has_children,
                StoragePlace.objects.exclude(barcode=None)
            )
        )
        response = self.client.post(
            "/api/v1/storages",
            {"name": "Supadupastorage",
             "parent": parent.id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_put_authorized_1(self):
        # rename
        self.billie_eilish_logs_in()
        some_storage = rchoice(StoragePlace.objects.all())
        storage_id = some_storage.id
        response = self.client.put(
            f"/api/v1/storages/{storage_id}",
            {"name": "Supadupastorage"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        the_same_storage = StoragePlace.objects.get(id=storage_id)
        self.assertEqual(the_same_storage.name, "Supadupastorage")

    def test_put_authorized_2(self):
        # move
        self.billie_eilish_logs_in()
        # some_storage, that is supposed to be moved into
        # parent_storage, shouldn't have children. Othervise
        # there will be needed descendance check. The same about
        # parent_storage to prevent name clash
        some_storage = rchoice(
            filter(
                lambda x: not x.has_children,
                StoragePlace.objects.all()
            )
        )

        # print(list(future_parent_storage_qset))
        parent_storage = rchoice_exclude(
            filter(
                lambda x: not x.has_children,
                StoragePlace.objects.filter(
                    barcode=None,
                )
            ),
            some_storage
        )
        response = self.client.put(
            f"/api/v1/storages/{some_storage.id}",
            {"parent": parent_storage.id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)
        some_storage_new = StoragePlace.objects.get(
            id=some_storage.id
        )
        self.assertEqual(some_storage_new.parent, parent_storage.id)

    def test_put_authorized_3(self):
        '''Attempt to put a storage into itself must end with 409'''
        self.billie_eilish_logs_in()
        storage = rchoice(StoragePlace.objects.all())
        storage_id = storage.id
        response = self.client.put(
            f"/api/v1/storages/{storage_id}",
            {"parent": storage_id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_put_authorized_4(self):
        '''Attempt to put a storage into its descendant 
        must end with 409'''
        self.billie_eilish_logs_in()
        child = None

        while not child:
            storage = rchoice(
                filter(
                    lambda x: x.has_children,
                    StoragePlace.objects.exclude(level=0)
                )
            )
            children = StoragePlace.objects.filter(
                parent=storage.id,
                barcode=None
            )
            if children.count() == 0:
                continue
            else:
                child = rchoice(children)

        response = self.client.put(
            f"/api/v1/storages/{storage.id}",
            {"parent": child.id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_put_authorized_5(self):
        '''Name clash inside of a storage between two child
        storages must end with 409'''
        self.billie_eilish_logs_in()
        parent_storage = rchoice(
            filter(
                lambda x: (x.has_children and
                    StoragePlace.objects.filter(
                        parent=x.id
                    ).count() >= 2
                ),
                StoragePlace.objects.filter(barcode=None)
            )
        )
        child_1 = rchoice(
            StoragePlace.objects.filter(
                parent=parent_storage.id
            )
        )
        child_2 = rchoice_exclude(
            StoragePlace.objects.filter(
                parent=parent_storage.id
            ),
            child_1
        )
        response = self.client.put(
            f"/api/v1/storages/{child_1.id}",
            {"name": child_2.name},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)
    
    def test_put_authorized_6(self):
        self.billie_eilish_logs_in()
        parent = rchoice(
            StoragePlace.objects.exclude(barcode=None)
        )
        new_child = rchoice_exclude(
            filter(
                lambda x: not x.has_children,
                StoragePlace.objects.all()
            ),
            parent
        )
        response = self.client.put(
            f'/api/v1/storages/{new_child.id}',
            {"parent": parent.id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 409)

    def test_post_unauthorized(self):
        parent_storage = rchoice(
            StoragePlace.objects.filter(barcode=None)
        )
        response = self.client.post(
            "/api/v1/storages",
            {"name": "Supadupastorage",
             "parent": parent_storage.id},
             content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_put_unauthorized_1(self):
        '''Trying rename storage being unauthorized. 
        Must end with 403'''
        storage = rchoice(
            StoragePlace.objects.all()
        )
        response = self.client.put(
            f"/api/v1/storages/{storage.id}",
            {"name": "Supadupastorage"},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_put_unauthorized_2(self):
        '''Trying move storage being unauthorized. 
        Must end with 403'''
        will_be_moved = rchoice(
            filter(
                lambda x: not x.has_children,
                StoragePlace.objects.all()
            )
        )
        parent = rchoice_exclude(
            filter(
                lambda x: not x.has_children,
                StoragePlace.objects.all()
            ),
            will_be_moved
        )
        response = self.client.put(
            f"/api/v1/storages/{will_be_moved.id}",
            {"parent": parent.id},
            content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)

    def test_delete_authorized_1(self):
        self.billie_eilish_logs_in()
        storage = rchoice(
            filter(
                lambda x: Chemical.objects.filter(
                    storage_place=x
                ).count() > 0,
                StoragePlace.objects.exclude(barcode=None)
            )
        )
        response = self.client.delete(
            f"/api/v1/storages/{storage.id}"
        )
        self.assertEqual(response.status_code, 409)

    def test_delete_authorized_2(self):
        self.billie_eilish_logs_in()
        storage = rchoice(
            filter(
                lambda x: x.has_children,
                StoragePlace.objects.filter(barcode=None)
            )
        )
        response = self.client.delete(
            f"/api/v1/storages/{storage.id}"
        )
        self.assertEqual(response.status_code, 409)

    def test_delete_authorized_3(self):
        self.billie_eilish_logs_in()
        storage = rchoice(
            filter(
                lambda x: (
                    not x.has_children and
                    Chemical.objects.filter(
                        storage_place=x
                    ).count() == 0
                ),
                StoragePlace.objects.all()
            )
        )
        response = self.client.delete(
            f"/api/v1/storages/{storage.id}"
        )
        self.assertEqual(response.status_code, 204)


    def test_delete_unauthorized(self):
        storage = rchoice(
            filter(
                lambda x: (
                    not x.has_children and
                    Chemical.objects.filter(
                        storage_place=x
                    ).count() == 0
                ),
                StoragePlace.objects.exclude(barcode=None)
            )
        )
        response = self.client.delete(
            f"/api/v1/storages/{storage.id}"
        )
        self.assertEqual(response.status_code, 403)
