from django.db import models
from django.urls import reverse
import uuid
from django.contrib.auth.models import User
from datetime import date
from django.db.models import Sum


# Create your models here.



class Genre(models.Model):
    """Model representing a book genre."""
    name = models.CharField(max_length=200, help_text='Enter a book genre (e.g. Science Fiction)')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.book_id}, {self.book.title},{self.name}'

class Category(models.Model):
    """Model representing a book category."""
    name = models.CharField(max_length=200, help_text='Enter a book category (e.g. Best seller)')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.book_id}, {self.book.title},{self.name}'

class Ratings(models.Model):
    """Model representing a book rating."""
    name = models.CharField(max_length=200, help_text='Enter a book rating')
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.book_id}, {self.book.title},{self.name}'

class Book(models.Model):
    """Model representing a book (but not a specific copy of a book)."""
    book_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular book across whole library')
    title = models.CharField(max_length=200)
    
    # Foreign Key used because book can only have one author, but authors can have multiple books
    # Author as a string rather than object because it hasn't been declared yet in the file
    author = models.ForeignKey('Author', on_delete=models.SET_NULL, null=True)

    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN', max_length=13, unique=True,
                             help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')

    
    # Genre class has already been defined so we can specify the object above.
    PublYear = models.CharField(max_length=200)
    

    def get_absolute_url(self):
        """Returns the url to access a detail record for this book."""
        return reverse('book-detail', args=[str(self.book_id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book_id} {self.title} '



class BookInstance(models.Model):
    """Model representing a specific copy of a book (i.e. that can be borrowed from the library)."""
    
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    

    LOAN_STATUS = (
        ('m', 'Maintenance'),
        ('o', 'On loan'),
        ('a', 'Available'),
        ('r', 'Reserved'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='m',
        help_text='Book availability',
    )

    class Meta:
        ordering = ['due_back']
        permissions = (("can_view_all_borrowed_books", "All borrowed Books"),)

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book_id} ({self.book.title})'
    
    @property
    def is_overdue(self):

        if self.due_back and date.today() > self.due_back:
            return True
        return False


class Author(models.Model):
    """Model representing an author."""
    author_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular author across whole library')
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    bio_data =  models.TextField(max_length=1000, help_text='Enter a brief description of the author')
   
  
    

    class Meta:
        ordering = ['last_name', 'first_name']

    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.author_id)])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.last_name}, {self.first_name}'


class InStock(models.Model):

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    how_many_left = models.CharField(max_length=200)


    class Meta:
        ordering = ['how_many_left']


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.book_id}, {self.book.title},{self.how_many_left}'

class SoldOut(models.Model):

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    expected_date_of_availability = models.CharField(max_length=200)


    class Meta:
        ordering = ['expected_date_of_availability']


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.book_id}, {self.book.title},{self.expected_date_of_availability}'


class Likes(models.Model):

    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    recommended_books= models.CharField(max_length=200)


    class Meta:
        ordering = ['recommended_books']


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.book.book_id}, {self.book.title},{self.recommended_books},{self.buyer}'

class Orders(models.Model):


    order_id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular order across whole library')
    items = models.ManyToManyField(Book)
    date_ordered = models.DateTimeField(auto_now=True)
    is_ordered = models.BooleanField(default=False)

    STATUS = (
        ('COD', 'Cash on Delivery'),
        ('card', 'Card'),
    )

    payment_method = models.CharField(
        max_length=5,
        choices=STATUS,
        blank=False,
        default='COD',
        help_text='Payment Method',
    )


    class Meta:
        ordering = ['payment_method']

    

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        return sum([item.book.price for item in self.items.all()])

    def __str__(self):
        """String for representing the Model object."""
        return f'{self.payment_method}, {self.order_id}'


class HardBookOrders(models.Model):

    orders = models.ForeignKey('Orders', on_delete=models.SET_NULL, null=True)
    delivery_address= models.CharField(max_length=200)


    class Meta:
        ordering = ['delivery_address']


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.orders.order_id}, {self.delivery_address}'

class ActiveOrders(models.Model):

    orders = models.ForeignKey('Orders', on_delete=models.SET_NULL, null=True)
    expected_delivery_date= models.DateField(null=True, blank=True)


    class Meta:
        ordering = ['expected_delivery_date']


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.orders.order_id}, {self.expected_delivery_date}'

class CompletedOrders(models.Model):

    orders = models.ForeignKey('Orders', on_delete=models.SET_NULL, null=True)
    received_by= models.CharField(max_length=200)


    class Meta:
        ordering = ['received_by']


    def __str__(self):
        """String for representing the Model object."""
        return f'{self.orders.order_id}, {self.received_by}'

class Purchase(models.Model):

    orders = models.ForeignKey('Orders', on_delete=models.SET_NULL, null=True)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    buyer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self):
        """String for representing the Model object."""
        return f'{self.orders.order_id}, {self.book.book_id},{self.buyer}'









class Customer(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.CharField(max_length=200,null=True, blank=True)

    def __str__(self):
        return self.name
    


class Order(models.Model):
    customer=models.ForeignKey('Customer',on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False, null=True, blank=False)
    transaction_id=models.CharField(max_length=200,null=True)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems=self.orderitem_set.all()
        total=sum([item.quantity for item in orderitems])
        return total

class Product(models.Model):

    name=models.ForeignKey('Book',on_delete=models.SET_NULL, null=True)
    price=models.FloatField()
    digital=models.BooleanField(default=False, null=True, blank=False)
    
    def __str__(self):
        return str(self.name)


class OrderItem(models.Model):
    product=models.ForeignKey('Product',on_delete=models.SET_NULL, null=True)
    order=models.ForeignKey('Order',on_delete=models.SET_NULL, null=True)
    quantity=models.IntegerField(default=0,null=True, blank=True)
    date_added=models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total=self.product.price * self.quantity
        return total
    
class ShippingAddress(models.Model):
    customer = models.ForeignKey('Customer',on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey('Order',on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200,null=False)
    city = models.CharField(max_length=200,null=False)
    state = models.CharField(max_length=200,null=False)
    zipcode = models.CharField(max_length=200,null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address
