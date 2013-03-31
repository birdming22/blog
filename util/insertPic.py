# generate picture url for jekyll post

import os
import hashlib
try:
    from dulwich.repo import Repo
    from dulwich.index import changes_from_tree
except:
    print 'install dulwich first'
    print 'https://github.com/jelmer/dulwich'

def getFileList(path):
    fileList = []
    for root, dirs, files in os.walk(path):
        # fixme: remove exclusive file
        if '.git' in dirs:
            dirs.remove('.git')
        if len(files) != 0:
            fileList += [os.path.join(root, wc) for wc in files]
    return fileList

def main():
    currentDir = os.getcwd()
    PROJECT_PATH = os.path.abspath(os.path.join(currentDir, os.pardir))
    BLOG_PATH = PROJECT_PATH + '/blog'
    IMG_PATH = PROJECT_PATH + '/img'

    repo = Repo(PROJECT_PATH)
    treeId = repo['HEAD'].tree
    treeIter = repo.object_store.iter_tree_contents(treeId)
    fileList = getFileList(IMG_PATH)

    '''
    for f in fileList:
        print f
    '''

    def lookup_entry(name):
        if name not in fileList:
            raise(KeyError)
        else:
            name = os.path.join(repo.path, name)
            with open(name,'rb') as GitFile:
                data = GitFile.read()
                s = hashlib.sha1()
                s.update("blob %u\0" % len(data))
                s.update(data)
            return (s.hexdigest() , os.stat(name).st_mode)
    result = changes_from_tree(fileList, lookup_entry, repo.object_store, treeId, want_unchanged=False)
    # fixme: added_files is wrong
    for (name, mode, sha) in result:
        print name, mode, sha
    '''
    added_files = ([(name[1], mode[1], sha[1]) for (name, mode, sha) in result
                   if name[0] is None and name[1] is not None])
    for (name, mode, sha) in added_files:
        print '#       new file:   %s' % name
    '''
    #index = repo.open_index()
    #tree = repo.tree(sha)
    #print list(tree)
    '''
    sha = repo.ref('refs/heads/gh-pages')
    print sha

    for ref in repo.refs.keys('refs/heads/'):
        print ref
    #changes = index.changes_from_tree(repo.object_store, repo['gh-pages'].tree)
    #print list(changes)
    for item in index.iteritems():
        print item
    '''


if __name__ == "__main__":
    main()

'''
    Reference: https://github.com/mikofski/dulwichPorcelain
'''
