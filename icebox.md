MEAL_TYPE = (
    ('B', 'Breakfast'),
    ('L', 'Lunch'),
    ('D', 'Dinner')
)

class CollabGroup(models.Model):
    name = models.CharField(max_length=100)
    members = models.ManyToManyField(CustomUser)
    REQUIRED_FIELDS = ['name']

    def __str__(self):
        return self.name
    
class Recipes(models.Model):
    title = models.CharField(max_length=150)
    url = models.URLField(max_length=200)
    ingredients = models.JSONField(default=list)
    instructions = models.JSONField(default=list)
    collab_group = models.ForeignKey(CollabGroup, on_delete=models.CASCADE)
    REQUIRED_FIELDS = ['title', 'ingredients', 'instructions']

    def __str__(self):
        return self.title    

class Meal(models.Model):
    type = models.CharField(max_length=1, choices=MEAL_TYPE, default=MEAL_TYPE[0][0])
    date = models.DateField()
    recipe = models.ForeignKey(Recipes, on_delete=models.PROTECT)
    collab_group = models.ForeignKey(CollabGroup, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.type[1]} {self.date}"