import os
import sys
import argparse


def log_error(err_msg=None):
    if err_msg is not None:
        print 'ERROR: ' + err_msg
    sys.exit(1)


def parse_arguments():
    argparser = argparse.ArgumentParser()

    argparser.add_argument('-i', '--input-dir', metavar='input_dir', help='PcapPlusPlus-Doc directory')
    argparser.add_argument('-o', '--output-dir', metavar='output_dir', help='Destination directory')

    args = argparser.parse_args()

    if args.output_dir is None:
        log_error('Please set output directory')

    if not os.path.isdir(args.output_dir):
        log_error('Cannot find dir ' + args.output_dir + ' Exiting...')

    if args.input_dir is None:
        args.input_dir = os.getcwd()

    args.output_dir = os.path.abspath(args.output_dir)

    if args.output_dir == args.input_dir:
        log_error('Input and output directories cannot be equal')

    print 'input_dir=', args.input_dir
    print 'output_dir=', args.output_dir

    return args


def copy_dirs(input_dir, output_dir):
    print 'coping "resources" dir...',
    if os.system('cp -rf ' + input_dir + '/resources ' + output_dir) != 0:
        log_error()
    print 'done!'

    print 'coping "Documentation" dir...',
    if os.system('cp -rf ' + input_dir + '/Documentation ' + output_dir) != 0:
        log_error()
    print 'done!'

    print 'coping "style" dir...',
    if os.system('cp -rf ' + input_dir + '/style ' + output_dir) != 0:
        log_error()
    print 'done!'


def read_layout_content(input_dir):
    layout_filename = input_dir + '/_layouts/default.html'
    if not os.path.isfile(layout_filename):
        log_error('cannot find layout file in path: ' + layout_filename)

    with open(layout_filename, 'r') as layout_file:
        return layout_file.read()


def parse_html_file(input_dir, filename):
    header = {}
    content = ''
    with open(input_dir + '/' + filename, 'r') as cur_file:
        lines = cur_file.readlines()
        header_start = False
        for line in lines:
            if line.startswith('---'):
                header_start = not header_start
                continue

            if header_start is True:
                key_value = line.split(':')
                header[key_value[0].strip().replace('\n','')] = key_value[1].strip().replace('\n','')
                continue
            else:
                content = content + line

    return header, content
           


def build_html_file(input_dir, filename, layout_content, output_dir):
    header, content = parse_html_file(input_dir, filename)
    new_content = layout_content.replace('{{ content }}', content)
    title = header.get('title')
    section = header.get('section')
    if title is not None:    
        new_content = new_content.replace('{{ page.title }}', header.get('title'))
    if section is not None:
        new_content = new_content.replace('{{ page.section }}', header.get('section'))
    with open(output_dir + '/' + filename, 'w') as output_file:
        output_file.write(new_content)


if __name__ == '__main__':
    # main method

    args = parse_arguments()

    output_dir = args.output_dir + '/PcapPlusPlus-WebSite'
    print 'creating "PcapPlusPlus-WebSite" dir...',
    if os.system('mkdir ' + output_dir) != 0:
        log_error()
    print 'done!'

    copy_dirs(args.input_dir, output_dir)

    layout_content = read_layout_content(args.input_dir)

    for filename in os.listdir(args.input_dir):
        if filename.endswith('.html'):
            print 'building "' + os.path.abspath(filename) + '"...',
            build_html_file(args.input_dir, filename, layout_content, output_dir)
            print 'done!'

    print 'Finished successfuly!'
