import random
import requests

# burst 15 requests for different shady uris
def uri_enumeration(target, source_ip, user_agent, **kwargs):

    uris = ['index', 'payment', 'config.php', 'main', 'secure', 'enumerate', 'danger', 'images', 'admin',
            'includes', 'search', 'cache', 'login', 'modules', 'templates', 'plugins', 'stats', 'forum', 'test',
            'download', 'comments', 'profile', 'private', 'include', 'category', 'logout', 'comment', 'report',
            'tag', 'member', 'add', 'update', 'img', 'password', 'calendar', 'rss', 'LICENSE', 'memberlist',
            'profiles', 'reply', 'node', 'ajax', 'INSTALL', 'files', 'CHANGELOG', 'UPGRADE', 'MAINTAINERS',
            'image', 'account', 'logs', 'data', 'faq', 'blog', 'cart', 'help', 'temp', 'newreply', 'sites',
            'newthread', 'objects', 'dyn', 'config', 'usercp', '_private', 'inc', 'page', 'online', 'news',
            'aspnet_client', 'editpost', 'sendmessage', 'wp-login', 'subscription', 'lib', 'go', 'author',
            'attachment', 'poll', 'uploads', 'threadrate', 'printthread', 'error', 'catalog', 'modcp',
            'checkout', 'flash', '404', 'docs', 'moderator', 'showgroups', 'joinrequests', 'members', 'privacy',
            'postings', 'backup', 'reputation', 'global', 'Templates', 'editor', 'print', 'downloads', 'content',
            'links', 'home', 'admincp', 'newsletter', 'upload', 'api', 'en', 'common', 'styles', 'pdf', 'email',
            'template', 'usernote', 'archive', 'forums', 'redirect', 'gallery', 'newattachment', 'inlinemod',
            'create_account', 'db', 'shop', 'ads', 'Scripts', 'assets', 'shopping_cart', 'view', 'wp-register',
            'tools', 'tags', 'about', 'pub', 'statistics', 'recommend', 'order', 'posting', 'archives',
            'mambots']

    headers = {'User-Agent': user_agent,
               'True-Client-IP': str(source_ip)
              }

    ret = ""
    for i in range(15):
        bad_uri = random.choice(uris)
        response = requests.get(target + "/" + bad_uri, headers=headers).status_code
        ret += "uri_enumeration: got {} with /{}\n".format(response,bad_uri)
    return(ret)
