import getpass
import re

def read_lines_from_file(file_path):
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def add_x_status_f_to_emails(mail_file_path, links_to_detect, allowed_attachments):
    with open(mail_file_path, 'r') as file:
        emails = file.read().split('\n\nFrom ')

    modified_emails = []
    for email in emails:
        lines = email.split('\n')
        email_content = '\n'.join(lines[lines.index('')+1:]) if '' in lines else ''
        
        flag_email = False
        
        if any(link in email_content for link in links_to_detect):
            flag_email = True
        
        if 'Content-Type: multipart/mixed;' in email:
            boundary_match = re.search(r'boundary="([^"]+)"', email)
            if boundary_match:
                boundary = boundary_match.group(1)
                parts = email.split('--' + boundary)
                for part in parts:
                    if 'Content-Disposition: attachment;' in part:
                        filename_match = re.search(r'filename="([^"]+)"', part, re.IGNORECASE)
                        if filename_match:
                            filename = filename_match.group(1)
                            extension = filename.split('.')[-1].lower()
                            if extension not in allowed_attachments:
                                flag_email = True
                                break
        
        if flag_email:
            x_status_lines = [line for line in lines if line.startswith('X-Status:')]
            if x_status_lines:
                x_status_index = lines.index(x_status_lines[0])
                if 'F' not in lines[x_status_index]:
                    lines[x_status_index] += 'F'
            else:
                blank_line_index = lines.index('')
                lines.insert(blank_line_index, 'X-Status: F')

        modified_emails.append('\n'.join(lines))

    with open(mail_file_path, 'w') as file:
        file.write('\n\nFrom '.join(modified_emails))

current_user = getpass.getuser()

detect_file_path = "/srv/shared/phishingTool/detect.txt"
attachments_file_path = "/srv/shared/phishingTool/attachments.txt"
user1_mail_file_path = f'/var/mail/{current_user}'

links_to_detect = read_lines_from_file(detect_file_path)
allowed_attachments = read_lines_from_file(attachments_file_path)

add_x_status_f_to_emails(user1_mail_file_path, links_to_detect, allowed_attachments)

