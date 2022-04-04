# Copyright (c) 2022, michael.hutchons@gmail.com and contributors
# For license information, please see license.txt
# This is pretty awesome!

#import frappe
from frappe.model.document import Document

class LibraryMember(Document):
	def before_naming(self):
		self.full_name = f'{self.first_name} {self.last_name or ""}'
