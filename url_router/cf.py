# a custom page rourt to support multi language

from frappe.website.path_resolver import resolve_path as original_resolve_path
import frappe


def resolve_path(path):
    
    if path and '.js' not in path:
        # get the first part of the path
        url_parts = path.rsplit('/')
        #print('URL Parts: ' + str(url_parts))
        if url_parts:
            fpart = url_parts[0]
        else:
            fpart = ''
        #print('First Part: ' + fpart)
        
        # current language
        lang = str(frappe.lang)

        if fpart not in ['app', 'api', 'backups', 'files', 'private'] and fpart != lang:

            clean_path = path
            
            # check if the first part of the route contains langauge selection and remove it
            if len(fpart) == 2:
                clean_path = clean_path[3:]

            # remove qury parameters
            if '?' in clean_path:
                clean_path = clean_path.split('?')[0]
            if '#' in clean_path:
                clean_path = clean_path.split('#')[0]
            #print('Clean Path: ' + clean_path)

            # get list of Web Pages
            web_routes = frappe.db.get_all('Web Page',
                            filters={
                                'published': 1,
                            },
                            pluck='route')
            
            for route in web_routes:

                if route.endswith(clean_path):
                    # Calculate the difference
                    diff = route[:len(route) - len(clean_path)]
                    if diff.endswith('/') and len(diff) == 3 and diff[:2] == lang:
                        path = route
                        #print('New Path: ' + path)
                        break

    return original_resolve_path(path)
