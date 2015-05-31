from meetup_wrapper import meetup
from datetime import datetime
from unittest import TestCase
from unittest.mock import patch
import json


class TestMeetupClient(TestCase):

    def test_connection(self):
        """ Integration test """
        client = meetup.MeetupClient()
        http_response = client.get_response(group_urlname='Buenos-Aires-Python-Meetup')
        self.assertEqual(http_response.status, 200)

    @patch('meetup_wrapper.meetup.MeetupClient')
    def test_events(self, mock_get):
        with open('tests/resources/response.json') as response_file:
            mock_get.return_value.get_events.return_value = json.loads(response_file.read())

            client = meetup.MeetupClient()
            json_response = client.get_events(group_urlname='Buenos-Aires-Python-Meetup')

            self.assertEqual('Charlas, Mates y Sprints!', json_response.get('results')[0].get('name'))
            self.assertEqual('http://www.meetup.com/Buenos-Aires-Python-Meetup/events/222357366/',
                             json_response.get('results')[0].get('event_url'))
            self.assertEqual("""<p>Vuelve el Buenos Aires Python Meetup. En esta oportunidad vamos a juntarnos todo un Sábado."""
                            """<br/>Por la mañana vamos a tener charlas, al mediodía cortamos para charlar entre nosotros, comer algo, tomar unos """
                            """mates y por la tarde sprints! A programar hasta que nos inviten a retirarnos.</p> <p>\n\n\nDetalle de las charlas: """
                            """<a href="http://listas.python.org.ar/pipermail/pyar/2015-May/034610.html">"""
                            """<a href="http://listas.python.org.ar/pipermail/pyar/2015-May/034610.html" class="linkified">"""
                            """http://listas.python.org.ar/pipermail/pyar/2015-May/034610.html</a></a></p> <p><br/>Los esperamos!</p>""",
                            json_response.get('results')[0].get('description'))

            self.assertEqual('222357366', json_response.get('results')[0].get('id'))
            start = json_response.get('results')[0].get('time')
            duration = json_response.get('results')[0].get('duration')
            self.assertEqual(1432990800000, start)
            self.assertEqual(28800000, duration)
            self.assertEqual(datetime(2015, 5, 30, 10), datetime.fromtimestamp(start / 1000))
            self.assertEqual(datetime(2015, 5, 30, 18), datetime.fromtimestamp((start + duration) / 1000))


if __name__ == '__main__':
    unittest.main()
