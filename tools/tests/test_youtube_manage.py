import contextlib, io, sys, unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import Mock, patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import youtube_manage as m

class ManagementChecks(unittest.TestCase):
    def setUp(self):
        self.video={'id':'v1','snippet':{'title':'Original','description':'Keep this','categoryId':'27','tags':['archive'],'defaultLanguage':'en','channelId':'UC1','thumbnails':{'default':{}}},'status':{'privacyStatus':'private','selfDeclaredMadeForKids':False,'containsSyntheticMedia':True,'uploadStatus':'processed','license':'youtube'}}

    def test_title_patch_preserves_description_tags_language(self):
        body=m.metadata_body(self.video,{'title':'Revised'})
        self.assertEqual(body['snippet']['description'],'Keep this')
        self.assertEqual(body['snippet']['tags'],['archive'])
        self.assertEqual(body['snippet']['defaultLanguage'],'en')
        self.assertNotIn('channelId',body['snippet'])
        self.assertNotIn('thumbnails',body['snippet'])
        self.assertEqual(self.video['snippet']['title'],'Original')

    def test_patch_rejects_unrelated_status(self):
        with self.assertRaises(ValueError): m.metadata_body(self.video,{'privacyStatus':'public'})

    def test_schedule_preserves_disclosures_and_normalizes_timezone(self):
        future=(datetime.now(timezone.utc)+timedelta(days=2)).isoformat()
        status=m.visibility_body(self.video,'private',future)['status']
        self.assertTrue(status['containsSyntheticMedia'])
        self.assertFalse(status['selfDeclaredMadeForKids'])
        self.assertEqual(status['license'],'youtube')
        self.assertNotIn('uploadStatus',status)
        self.assertTrue(status['publishAt'].endswith('Z'))

    def test_schedule_rejects_past_naive_or_public(self):
        for privacy,when in [('private','2000-01-01T00:00:00Z'),('private','2099-01-01T00:00:00'),('public','2099-01-01T00:00:00Z')]:
            with self.subTest(privacy=privacy,when=when),self.assertRaises(ValueError): m.visibility_body(self.video,privacy,when)

    def test_wrong_channel_rejected(self):
        yt=Mock()
        yt.channels.return_value.list.return_value.execute.return_value={'items':[{'id':'UC_OTHER'}]}
        with self.assertRaises(ValueError): m.own_channel(yt,'UC1')

    def test_other_channels_video_rejected(self):
        yt=Mock()
        yt.videos.return_value.list.return_value.execute.return_value={'items':[self.video]}
        with self.assertRaises(ValueError): m.owned_video(yt,'v1','UC_OTHER')

    def test_default_metadata_command_never_writes(self):
        yt=Mock()
        with patch.object(sys,'argv',['youtube_manage.py','metadata','--channel','UC1','--video','v1','--file','patch.json']),patch.object(m,'service',return_value=yt) as svc,patch.object(m,'own_channel'),patch.object(m,'owned_video',return_value=self.video),patch.object(m,'load',return_value={'title':'Revised'}),patch.object(m,'save_plan',return_value='review-plan.json'),contextlib.redirect_stdout(io.StringIO()) as output:
            m.main()
        svc.assert_called_once_with('read')
        yt.videos.assert_not_called()
        self.assertIn('"dry_run": true',output.getvalue())

    def test_status_never_authenticates(self):
        with patch.object(sys,'argv',['youtube_manage.py','status']),patch.object(m,'credentials') as auth,contextlib.redirect_stdout(io.StringIO()): m.main()
        auth.assert_not_called()

if __name__=='__main__': unittest.main()
