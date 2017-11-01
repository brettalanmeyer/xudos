import math

class PagedService():

	def paged(self, records, page = 1, limit = 20, width = 4):
		total = records.count()
		pages = int(math.ceil(total / float(limit)))
		offset = (page - 1) * limit

		return {
			"records": records.limit(limit).offset(offset).all(),
			"total": total,
			"page": page,
			"limit": limit,
			"pages": pages,
			"width": width
		}
