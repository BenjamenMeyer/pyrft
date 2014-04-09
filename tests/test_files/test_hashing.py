"""
Test File hash
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

import unittest
import random
import os
import os.path
import pyrft.files.data


class TestHashing(unittest.TestCase):

	def setUp(self):
		self.inputFileName = 'test1gb.dat'
		self.outputFileName = 'test1gb.out'
		self.metadata = None
		max_length = 1 * 1024 * 1024 * 1024
		with open(self.inputFileName, 'a+b') as random_data:
			while random_data.tell() < max_length:
				d = str(random.randint(0, 4294967295))
				for x in xrange(256):
					random_data.write(d)

	def test_build_metadata(self):
		#   1KB = 1024
		# 512KB = 512*1024
		#   1MB = 1024*1024
		#   2MB = 2*1024*1024
		#   4MB = 4*1024*1024
		#   8MB = 8*1024*1024
		#  16MB = 16*1024*1024
		#  25MB = 32*1024*1024
		#  64MB = 64*1024*1024
		# 128MB = 128*1024*1024
		# 256MB = 256*1024*1024
		# 512MB = 512*1024*1024
		boundaries = [ 1024,
					   512*1024,
					   1024*1024,
					   2*1024*1024,
					   4*1024*1024,
					   8*1024*1024,
					   16*1024*1024,
					   32*1024*1024,
					   64*1024*1024,
					   128*1024*1024,
					   256*1024*1024,
					   512*1024*1024
					   ]
		for boundary in boundaries:
			yield _build_meta_data, self, boundary

	def _build_meta_data(self, bound_size):
		meta_data_builder = pyrft.files.data.FileData('.', self.inputFileName, bound_size=bound_size)
		meta_data_builder.gnerate_file_metadata()
		meta_data = meta_data_builder.getMetaData()
	
	def tearDown(self):
		#if os.path.exists(self.inputFileName):
		#	os.remove(self.inputFileName)
		if os.path.exists(self.outputFileName):
			os.remove(self.outputFileName)

