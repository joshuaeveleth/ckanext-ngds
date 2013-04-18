from ckan.lib.base import model,h,g,c,request
import ckan.lib.navl.dictization_functions as dictization_functions
import ckanext.ngds.geoserver.logic.action as geoserver_actions
import ckan.logic as logic
import ckan.controllers.storage as storage
DataError = dictization_functions.DataError
NotFound = logic.NotFound
from pylons import config


def get_responsible_party_name(id):
	"""
	Get the name of a responsible party for an id.
	"""
	# If we don't get an int id, return an empty string.
	if id:
		try:
			id_int = int(id)
		except(ValueError):
			return ""
		responsible_party = model.ResponsibleParty.get(id)
		if responsible_party:
			return responsible_party.name
		else:
			return ""
	else:
		return ""

def get_login_url():
	x = request.url
	print x
	return h.url_for(_get_repoze_handler('login_handler_path'),came_from=x)

def _get_repoze_handler(handler_name):
    '''Returns the URL that repoze.who will respond to and perform a
    login or logout.'''
    return getattr(request.environ['repoze.who.plugins']['friendlyform'],handler_name)

def get_default_group():

	try:
		print g.default_group
	except AttributeError:
		g.default_group = config.get('ngds.default_group_name', 'public')

	return g.default_group

def get_language(id):
	if id:
		print "got id : "+id
		try:
			id_int = int(id)
		except(ValueError):
			return ""
		language = model.Language.get(id)
		print "Got language ",language
		print language.name
		if language:
			return language.name
		else:
			return ""
	else:
		return ""

def is_spatialized(res_id,col_geo):
	context = {'model': model, 'session': model.Session,\
                   'user': c.user or c.author, 'for_view': True}
	try:
		is_spatialized = geoserver_actions.datastore_is_exposed_as_layer(context,{'id':res_id})['is_exposed_as_layer']
		print is_spatialized
	except(NotFound):
		is_spatialized = False
	return is_spatialized

def get_url_for_file(label):
	# storage_controller = StorageController()
	BUCKET = config.get('ckan.storage.bucket', 'default')
	ofs = storage.get_ofs()
	return ofs.get_url(BUCKET,label)