import pandas as pd

def newsletter_yn(email_file) :
    everything = open(email_file, 'r')
    lines = list() #Lines of email file
    names_email = list() #Names of respondents for email extraction
    names_newsletter = list() #Names of respondents for newsletter extraction
    signups = list() #Newsletter signup status
    mess_ids_email = list() #Messenger IDs of respondents for email extraction
    mess_ids_newsletter = list() #Messenger IDs of respondents for email extraction
    emails = list() #Emails of respondents
    for line in everything :
        lines.append(line.rstrip())
    for pos, line in enumerate(lines) :
        if line == 'Subject: PIPD email signup' :
            name = lines[pos + 4][6:] #Names, emails
            names_email.append(name)
            email = lines[pos + 6][15:] #Emails
            emails.append(email)
            mess_id = lines[pos + 8][14:] #Messenger IDs, emails
            mess_ids_email.append(mess_id)
        if line == 'Subject: PIPD Messenger newsletter' :
            name = lines[pos + 4][6:] #Names, newsletter
            names_newsletter.append(name)
            signup = lines[pos + 6][12:] #Newsletter
            signups.append(signup)
            mess_id = lines[pos + 8][14:] #Messenger IDs, newsletter
            mess_ids_newsletter.append(mess_id)
    df_emails = pd.DataFrame()
    df_emails['Name (FB)'] = names_email
    df_emails['Messenger ID'] = mess_ids_email
    df_emails['Email'] = emails
    df_emails = df_emails.drop_duplicates('Messenger ID', keep = 'first')
    df_newsletters = pd.DataFrame()
    df_newsletters['Name (FB)'] = names_newsletter
    df_newsletters['Messenger ID'] = mess_ids_newsletter
    df_newsletters['Newsletter'] = signups
    df_newsletters = df_newsletters.drop_duplicates('Messenger ID', keep = 'first')
    df = df_emails.merge(df_newsletters, on = ['Name (FB)', 'Messenger ID'], how = 'outer').fillna('Not provided').set_index('Name (FB)')
    return df

#PRINT RESULTS
#print (newsletter_yn('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Email signups/PIPD_email_signups_7Feb.txt'))

#WRITE TO CSV
newsletter_yn('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Email signups/PIPD_email_signups_7Feb.txt').to_csv('/Users/jbachlombardo/Documents/Tere International/Clients/PIPD/Email signups/Email_signups_7Feb18.csv')
