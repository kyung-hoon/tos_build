#!/usr/bin/python3

import os, json, sys, getopt, tarfile, shutil, urllib.parse

metadata = {
    'application_type': 'web_view',
    'extensions': [],
    'title': {},
    'type':'E',
    'version':{
        'min_tos_version':'3.12.8',
        'name':'1.0.0',
        'number':10000
    }
}

def usage():
    print('Usage: make-webapp [OPTION]')
    print('  -h, --help      \t: show this help')
    print('  -t, --tai       \t: make .tai (TmaxOS application installer) file after making the app')
    print('  -c, --clean     \t: clean-up .tap (TmaxOS application package) directory after making .tai')
    print('  --app=NAME     \t: provide name of the creating app (default = "COPApp")')
    print('  --web=URL       \t: provide URL of the web page (default = local resource)')
    print('  --resource=DIR  \t: provide packaged web resources to load if $web = $app')
    print('  --corp=NAME     \t: provide corporation of the creating app (default = "TmaxA&C")')
    print('  --developer=NAME\t: provide developer of the creating app (default = $corp)')
    print('  --title=TITLE   \t: provide basic title of the creating app (default = $app')

def main(argv):
    makeTai = False
    cleanTap = False
    webResource = None
    try:
        opts, args = getopt.getopt(argv, 'cht', ['clean', 'help', 'web=', 'name=', 'resource=', 'tai'])
    except getopt.GetoptError:
        print('Invalid arguments.')
        usage()
        sys.exit(1)
    for opt, arg in opts:
        if opt in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif opt in ('-t', '--tai'):
            makeTai = True
        elif opt in ('-c', '--clean'):
            cleanTap = True
        elif opt == '--resource':
            webResource = arg
        elif opt.startswith('--'):
            cur = metadata;
            for key in opt.lstrip('-').split('.'):
                cur = cur[key]
            cur = arg

    appName = metadata.setdefault('app', 'COPApp')
    corp = metadata.setdefault('corp', 'TmaxA&C')
    metadata.setdefault('developer', corp)
    basic = metadata['title'].setdefault('basic', appName)
    webURL = metadata.setdefault('web', appName)

    scheme = urllib.parse.urlparse(webURL).scheme
    if not scheme or scheme is 'file':
        if not webResource:
            print('Missing "resource" option to be local resources')
            usage()
            sys.exit(1)
        elif not os.path.exists(webResource):
            print('Missing resource path: ' + webResource)
            usage()
            sys.exit(1)

    tapdir = appName + '.tap'
    try:
        os.mkdir(tapdir)
    except OSError:
        pass
    metafile = os.path.join(tapdir, '.metadata');
    with open(metafile, 'w') as outfile:
        json.dump(metadata, outfile, indent=2)
        print('Created "{}"'.format(tapdir))

    if webResource:
        shutil.copytree(webResource, os.path.join(tapdir, 'web', appName), symlinks=True)
        print('Web resource copied "{}"'.format(webResource))

    if makeTai:
        taifile = appName + '.tai'
        tar = tarfile.open(taifile, 'w:bz2')
        tar.add(tapdir)
        tar.close()
        print('Created "{}"'.format(taifile))

    if cleanTap:
        shutil.rmtree(tapdir)
        print('Deleted "{}"'.format(tapdir))

if __name__ == '__main__':
    main(sys.argv[1:])
