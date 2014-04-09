"""
Test File Data Object
Copyright 2014 Clockwerks Software, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

"""

import pyrft.files.data
import unittest

class test_file_data(unittest.TestCase):

	def test_file_data_constructor(self):
		t_path = "/tmp"
		t_file = "gotcha"
		bound = 1024

		file_data = pyrft.files.data.FileData(t_path, t_file, bound_size=bound)
		self.assertEqual(t_path, file_data.path)
		self.assertEqual(t_file, file_data.file_name)
		self.assertEqual('{0:}/{1:}'.format(t_path,t_file), file_data.fqfn)
		self.assertEqual(0, file_data.state)
		self.assertIsNone(file_data.metadata)

	def test_file_data_update_fqfn(self):
		t_path = '/tmp'
		t_file = 'beef'
		bound = 2048

		file_data = pyrft.files.data.FileData(t_path, t_file, bound_size=bound)
		self.assertEqual(t_path, file_data.path)
		self.assertEqual(t_file, file_data.file_name)
		self.assertEqual('{0:}/{1:}'.format(t_path,t_file), file_data.fqfn)

		file_data.path = '/opt/'
		file_data._FileData__update_fqfn()
		self.assertNotEqual('{0:}/{1:}'.format('/opt/',t_file), file_data.fqfn)
		self.assertEqual('{0:}{1:}'.format('/opt/',t_file), file_data.fqfn)

	def test_file_data_path(self):
		t_path = '/opt/devoid'
		t_file = 'beef'
		bound = 2048

		file_data = pyrft.files.data.FileData('/', 'dead', bound_size=bound)
		self.assertEqual('/', file_data.path)
		self.assertEqual('dead', file_data.file_name)
		self.assertEqual('/dead', file_data.fqfn)

		file_data.set_path(t_path)
		self.assertEqual(t_path, file_data.path)
		self.assertEqual('dead', file_data.file_name)
		self.assertEqual('{0:}/dead'.format(t_path), file_data.fqfn)

	def test_file_data_file(self):
		t_path = '/tmp'
		t_file = 'beef'
		bound = 2048

		file_data = pyrft.files.data.FileData(t_path, t_file, bound_size=bound)
		self.assertEqual(t_path, file_data.path)
		self.assertEqual(t_file, file_data.file_name)
		self.assertEqual('{0:}/{1:}'.format(t_path,t_file), file_data.fqfn)

		file_data.set_filename('dead')
		self.assertEqual(t_path, file_data.path)
		self.assertEqual('dead', file_data.file_name)
		self.assertEqual('{0:}/{1:}'.format(t_path,'dead'), file_data.fqfn)


	def test_file_data_metadata(self):
		t_path = '/tmp'
		t_file = 'beef'
		bound = 2048

		file_data = pyrft.files.data.FileData(t_path, t_file, bound_size=bound)
		self.assertIsNone(file_data.metadata)
		self.assertIsNone(file_data.getMetaData())
		self.assertEqual(file_data.metadata, file_data.getMetaData())

