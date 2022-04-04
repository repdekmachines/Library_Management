# Copyright (c) 2022, michael.hutchons@gmail.com and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.model.docstatus import DocStatus

class LibraryTransaction(Document):
	def before_submit(self):
		if self.type == "Issue":
			self.validate_issue()
			self.validate_maximum_limit()
			# set the article status to be issued
			article = frappe.get_doc("Article", self.article)
			article.status = "Issued"
			article.save()
		
		elif self.type == "Return":
			self.validate_return()
			# set the article status to be available
			article = frappe.get_doc("Article", self.article)
			article.status = "Available"
			article.save()


	def validate_issue(self):
		self.validate_membership()
		article = frappe.get_doc("Article", self.article)
		# article must not be issued if it is already issued
		if article.status == "Issued":
			frappe.throw("Article is already issued.")


	def validate_return(self):
		article = frappe.get_doc("Article", self.article)
		# article must be issued before it can be returned
		if article.status == "Available":
			frappe.throw("Article must be issued before it can be returned.")


	def validate_maximum_limit(self):
		max_articles = frappe.db.get_single_value("Library Settings", "max_articles")
		count = frappe.db.count(
			"Library Transaction",
			{"library_member": self.library_member, "type": "issue", "docstatus": DocStatus.submitted()},
		)
		if count >= max_articles:
			frappe.throw("Max limit reached for issued articles. Please return an Article first.")


	def validate_membership(self):
		# check if a valid membership exists for this user
		valid_membership = frappe.db.exists(
			"Library Membership",
			{
				"library_member": self.library_member,
				"docstatus": DocStatus.submitted(),
				"from_date": ("<", self.date),
				"to_date": (">", self.date),
			},
		)
		if not valid_membership:
			frappe.throw("No valid membership.")
