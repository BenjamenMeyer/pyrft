"""
PyRFT File Data Module
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
from __future__ import print_function
import hashlib
import os

class FileDataError(IOError):
	pass

class FileDataInvalidState(StandardError):
	pass

class FileDataPrepError(IOError):
	pass

class FileDataMetaDataError(IOError):
	pass

class FileData(object):
	"""
	File Data Information
	"""

	def state_at(state_level):  # pragma: nocover
		"""
		Decorator to ensure the class has the correct state before continuing
		"""
		def state_at_fn(fn):
			def check_state(self, *args, **kwargs):
				if self.state == state_level:
					result = fn(self, *args, **kwargs)
				else:
					raise FileDataInvalidState()
			return check_state
		return state_at_fn
	
	
	def state_raise(raiseState=True, lowerState=True):  # pragma: nocover
		"""
		Decorator to raise/lower the state for the duration of the call
		"""
		def state_raise_fn(fn):
			def raise_state(self):
				self.state = self.state + 1
			
			def lower_state(self):
				self.state = self.state - 1

			def do_call(self, *args, **kwargs):
				if raiseState:
					raise_state(self)
				result = fn(self, *args, **kwargs)
				if lowerState:
					lower_state(self)
				return result

			return do_call
		return state_raise_fn


	def __init__(self, path, file_name, bound_size=1024):
		self.boundary = bound_size
		self.path = path
		self.file_name = file_name
		self.__update_fqfn()
		self.state = 0
		self.metadata = None
	
	
	def __update_fqfn(self):  # pragma: nocover
		if self.path.endswith('/'):
			self.fqfn = '{0:}{1:}'.format(self.path, self.file_name)
		else:
			self.fqfn = '{0:}/{1:}'.format(self.path, self.file_name)

	
	
	@state_at(state_level=0)
	@state_raise()
	def set_path(self, path):
		self.path = path
		self.__update_fqfn()
	
	
	@state_at(state_level=0)
	@state_raise()
	def set_filename(self, file_name):
		self.file_name = file_name
		self.__update_fqfn()

	def __build_metadata(self, initial_position):
		self.metadata = {}
		fileinfo = os.stat(self.fqfn)
		self.metadata['file_info'] = {}
		self.metadata['file_info']['mtime'] = fileinfo.st_mtime
		self.metadata['file_info']['size'] = fileinfo.st_size
		hash_data = hashlib.sha256()
		self.metadata['hashes'] = {}
		with open(self.fqfn, 'rb') as input:
			# Move to the starting place in the file
			if initial_position:
				position  = 0
				while position < initial_position:
					buffer = input.read(1)
					if buffer:
						hash_data.update(buffer)
						# if on a boundary, then check the metdatdata
						position = input.tell()
						if mod(position, buffer) == 0:
							pos_hash = hash_data.copy()
							pos_hash_check = pos_hash.hexdigest()
							if pos_hash_check != self.metadata['hashes'][position]:
								raise FileDataMetaDataError('Hash does not match. Did the file change?')
					else:
						raise FileDataPrepError('Unable to seek to initial position')
			while True:
				# 1k chunks
				buffer = input.read(self.boundary)
				if buffer:
					hash_data.update(buffer)
					position = input.tell()
					pos_hash = hash_data.copy()
					self.metadata['hashes'][position] = pos_hash.hexdigest()
				else:
					break
		return True

	def __verify_metadata(self, position_start=None, position_end=None):
		with open(self.fqfn, 'rb') as input:
			# Move to the starting place in the file
			if initial_position:
				position  = 0
				while position < initial_position:
					buffer = input.read(self.boundary)
					if buffer:
						hash_data.update(buffer)
						position = input.tell()
						pos_hash = hash_data.copy()
						pos_hash_check = pos_hash.hexdigest()
						if pos_hash_check != self.metadata['hashes'][position]:
							raise FileDataMetaDataError('Hash does not match. Did the file change?')
					else:
						raise FileDataPrepError('Unable to seek to initial position')
		return True
	
	@state_at(state_level=0)
	@state_raise()
	def generate_file_metadata(self, initial_position=0):
			

		if self.metadata is None:
			return self.__build_metadata(initial_position)
		else:
			assert self.__verify_metadata(position_end=initial_position)
			return self.__build_metadata(initial_position)


	@state_at(state_level=0)
	@state_raise(lowerState=False)
	def start_file_transfer(self):
		pass
	
	@state_at(state_level=1)
	@state_raise(raiseState=False)
	def end_file_transfer(self):
		pass
	
	@state_at(state_level=1)
	def get_file_block(self, blockid=None):
		pass
	
	@state_at(state_level=0)
	def getMetaData(self):
		return self.metadata
	

"""
if __name__ == '__main__':
	f = FileData('/home/bmeyer/rft-test', 'test1gb.dat', bound_size=1024*1024)
	f.generate_file_metadata()
	with open('test.out', 'w') as out:
		import pprint
		pprint.pprint(f.getMetaData(), stream=out)
		import json
		print(json.dumps(f.getMetaData()),file=out)
	f.generate_file_metadata(4)
"""
