# Generated by Django 5.2.1 on 2025-05-17 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aviary', '0022_bonuscard_score_endroundgoal_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='bonus_cards',
            field=models.ManyToManyField(blank=True, related_name='bonus_cards', to='aviary.bonuscard'),
        ),
        migrations.AlterField(
            model_name='endroundgoal',
            name='goal',
            field=models.CharField(choices=[('NG', 'No Goal'), ('EF', 'Eggs in Forest'), ('EG', 'Eggs in Grassland'), ('EW', 'Eggs in Wetland'), ('BF', 'Birds in Forest'), ('BG', 'Birds in Grassland'), ('BW', 'Birds in Wetland'), ('BFC', 'Food Cost of Played Birds'), ('WFC', 'Worms in Food Cost'), ('CWFC', 'Cherries and Wheat in Food Cost'), ('FRFC', 'Fish and Rats in Food Cost'), ('BTC', 'Birds with Tucked Cards'), ('BRB', 'Birds with Brown Power'), ('WHB', 'Birds with White or No Power'), ('ECVTY', 'Eggs in Cavity Nests'), ('EBWL', 'Eggs in Bowl Nests'), ('ESTK', 'Eggs in Stick Nests'), ('EGRD', 'Eggs in Ground Nests'), ('CVTYBE', 'Cavity Nest Birds with Eggs'), ('BWLBE', 'Bowl Nest Birds with Eggs'), ('STKBE', 'Stick Nest Birds with Eggs'), ('GRDBE', 'Ground Nest Birds with Eggs'), ('BNE', 'Birds with No Eggs'), ('BGTF', 'Birds worth <4 points'), ('BLTF', 'Birds worth >4 points'), ('FIPS', 'Food in Personal Supply'), ('BIH', 'Bird Cards in Hand'), ('SE', 'Sets of Eggs'), ('FC', 'Filled Columns'), ('BIAR', 'Birds in one Row'), ('PLAYB', 'Number of Played Birds'), ('BPR', 'Beaks Pointing Right'), ('BPL', 'Beaks Pointing Left'), ('CPLAYB', 'Cubes on "Play a Bird"')], default='No Goal', max_length=50),
        ),
    ]
