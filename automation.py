from sr_misc.utils import CommitManually

__author__ = 'nisha'

import sys
import os
sys.path.append('/srv/www/appsphere')
os.environ['DJANGO_SETTINGS_MODULE']='settings'
from appsphere.settings import LOGGING_ROOT_DIRECTORY
from sr_callrecord.models import callrecord
from django.db import transaction
from django.utils import timezone
from datetime import timedelta
from django.db import connection,IntegrityError
import logging

logging.basicConfig(level=logging.DEBUG
        ,format='%(asctime)s [[%(levelname)s]] %(message)s'
        ,datefmt='%d %b %y %H:%M:%S'
        ,filename=LOGGING_ROOT_DIRECTORY + 'cdr_automation.log'
        ,filemode='a')

start_time=timezone.now()

while 1:

    with CommitManually():
        cdr_to_delete=[]
        query1='insert into SuperReceptionist_callrecord_backup select * from SuperReceptionist_callrecord where id '
        query2='insert into SuperReceptionist_sdrrecord_backup select * from SuperReceptionist_sdrrecord where cdr_id '
        query3='insert into SuperReceptionist_notificationrecord_backup select * from SuperReceptionist_notificationrecord where cdr_id '
        query4='delete from SuperReceptionist_notificationrecord where cdr_id '
        query5='delete from SuperReceptionist_sdrrecord where cdr_id '
        query6='delete from SuperReceptionist_callrecord where id '
        query7='select id from SuperReceptionist_callrecord_backup where id '
        try:
            cdr_to_delete=callrecord.objects.filter(start_time__lt=(timezone.now()-timedelta(days=190)))[:10].values_list('id','callid')
            logging.info('deleting following call records %s',cdr_to_delete)

            call_id_list=[]
            call_uuid_list=[]
            for call_ids in cdr_to_delete:
                call_id_list.append(call_ids[0])
                call_uuid_list.append(call_ids[1])
            if len(cdr_to_delete)==1:
                cdrquery='= %s'
            else:
                cdrquery='in %s'
                call_id_list=[call_id_list]
                call_uuid_list=[call_uuid_list]
            cursor = connection.cursor()
            try:

                cursor.execute(query1+cdrquery,call_id_list)
                cursor.execute(query2+cdrquery,call_id_list)
                cursor.execute(query3+cdrquery,call_uuid_list)
            except IntegrityError as e:
                if '(1062, "Duplicate entry ' in str(e):
                    logging.info('this is duplicate entry')
                    cursor.execute(query7+cdrquery,call_id_list)
                    cdr_in_backup=cursor.fetchall()
                    logging.info('cdr in backup %s call list %s'%(cdr_in_backup,call_id_list))
                    if (type(call_id_list[0]) is list and len(call_id_list[0])!=len(cdr_in_backup)) or (type(call_id_list[0]) is not list and len(call_id_list)!=len(cdr_in_backup)):
                        cdr_in_backuptable=list(sum(cdr_in_backup,()))
                        cdr_in_backup_list=[]
                        cdr_in_backup_uuid_list=[]
                        for call_ids in cdr_to_delete:
                            if call_ids[0] not in cdr_in_backuptable:
                                cdr_in_backup_list.append(call_ids[0])
                                cdr_in_backup_uuid_list.append(call_ids[1])
                        if len(call_id_list)==1:
                            cdrquery1='= %s'
                        else:
                            cdrquery1='in %s'
                            cdr_in_backup_list=[cdr_in_backup_list]
                            cdr_in_backup_uuid_list=[cdr_in_backup_uuid_list]
                        cursor.execute(query1+cdrquery1,cdr_in_backup_list)
                        cursor.execute(query2+cdrquery1,cdr_in_backup_list)
                        cursor.execute(query3+cdrquery1,cdr_in_backup_uuid_list)
                else:
                    raise

            cursor.execute(query4+cdrquery,call_uuid_list)
            cursor.execute(query5+cdrquery,call_id_list)
            cursor.execute(query6+cdrquery,call_id_list)
            cursor.close()
            transaction.commit()
        except Exception as e:
            logging.exception('transaction has been roll_backed for callrecords %s'%(cdr_to_delete))
            transaction.rollback()
            break

    if len(cdr_to_delete)<10 or (timezone.now()-start_time)>timedelta(minutes=22):
        logging.info('length of last set of cdr is %s and total script execution time is %s'%(len(cdr_to_delete),timezone.now()-start_time))
        break
