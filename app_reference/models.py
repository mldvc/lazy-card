from django.db import models


class Offices(models.Model):
    name = models.CharField("Office Name", max_length=200, unique=True)
    short = models.CharField("Abbreviation", max_length=10, unique=True)
    description = models.TextField("Description")

    class Meta:
        verbose_name = "Office"
        verbose_name_plural = "Offices"

    def __str__(self):
        return self.name


class IDTypes(models.Model):
    type = models.CharField("ID Type", max_length=200, unique=True)
    short = models.CharField("Abbreviation", max_length=10, unique=True)
    office = models.ForeignKey(Offices, on_delete=models.CASCADE)
    description = models.TextField("Description")

    class Meta:
        verbose_name = 'ID Type'
        verbose_name_plural = 'ID Types'

    def __str__(self):
        return self.type


class Departments(models.Model):
    dept = models.CharField("Department", max_length=200, unique=True)
    short = models.CharField("Abbreviation", max_length=10, unique=True)
    id_type = models.ManyToManyField(IDTypes, blank=True)
    description = models.TextField("Description")

    class Meta:
        verbose_name = 'Department'
        verbose_name_plural = 'Departments'

    def __str__(self):
        return self.dept


class Levels(models.Model):
    level = models.CharField("Level", max_length=200, unique=True)
    department = models.ForeignKey(Departments, on_delete=models.CASCADE)
    description = models.TextField("Description")

    class Meta:
        verbose_name = 'Level'
        verbose_name_plural = 'Levels'

    def __str__(self):
        return self.level


class Strands(models.Model):
    strand = models.CharField("Strand", max_length=200, unique=True)
    short = models.CharField("Abbreviation", max_length=10, unique=True)
    dept = models.ForeignKey(Departments, on_delete=models.CASCADE)
    description = models.TextField("Description")

    class Meta:
        verbose_name = 'Strand'
        verbose_name_plural = 'Strands'

    def __str__(self):
        return self.strand


class Courses(models.Model):
    course = models.CharField("Course", max_length=200, unique=True)
    short = models.CharField("Abbreviation", max_length=10, unique=True)
    dept = models.ForeignKey(Departments, on_delete=models.CASCADE)
    description = models.TextField("Description")

    class Meta:
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'

    def __str__(self):
        return self.course


class CardsLayout(models.Model):
    layout_name = models.CharField("Layout Name", max_length=200, unique=True)
    layout_code = models.CharField("Layout Code", max_length=200)
    layout_front = models.ImageField("Front Layout", upload_to='idlayouts/front')
    layout_back = models.ImageField("Back Layout", upload_to='idlayouts/back')
    id_type = models.ManyToManyField(IDTypes, blank=True)
    description = models.TextField("Description")

    class Meta:
        verbose_name = 'Card Layout'
        verbose_name_plural = 'Card layouts'

    def __str__(self):
        return self.layout_name


class EmploymentTypes(models.Model):
    emp_type = models.CharField("Employment Type", max_length=200, unique=True)
    layout = models.OneToOneField(CardsLayout)

    class Meta:
        verbose_name = 'Employment Type'
        verbose_name_plural = 'Emplotment Types'

    def __str__(self):
        return self.emp_type
