import getpass

def read_links_from_file(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

def add_x_status_f_to_emails(file_path, links_to_detect):
    with open(file_path, 'r') as file:
        emails = file.read().split('\n\nFrom ')

    modified_emails = []
    for email in emails:
        lines = email.split('\n')
        email_content = '\n'.join(lines[lines.index('')+1:])
        if any(link in email_content for link in links_to_detect):
            if 'X-Status: F' not in lines:
                blank_line_index = lines.index('')
                lines.insert(blank_line_index, 'X-Status: F')
        modified_emails.append('\n'.join(lines))

    with open(file_path, 'w') as file:
        file.write('\n\nFrom '.join(modified_emails))

current_user = getpass.getuser()

detect_file_path = "/home/{}/phishingTool/detect.txt".format(current_user)
user1_mail_file_path = '/var/mail/{}'.format(current_user)

links_to_detect = read_links_from_file(detect_file_path)

add_x_status_f_to_emails(user1_mail_file_path, links_to_detect)

