# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding field 'Book.price'
        db.add_column('book_book', 'price', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'Book.title'
        db.alter_column('book_book', 'title', self.gf('django.db.models.fields.CharField')(max_length=128))

        # Changing field 'Book.publication_date'
        db.alter_column('book_book', 'publication_date', self.gf('django.db.models.fields.DateTimeField')())

        # Deleting field 'Author.last_name'
        db.delete_column('book_author', 'last_name')

        # Deleting field 'Author.first_name'
        db.delete_column('book_author', 'first_name')

        # Adding field 'Author.name'
        db.add_column('book_author', 'name', self.gf('django.db.models.fields.CharField')(default=None, max_length=40), keep_default=False)

        # Changing field 'Author.email'
        db.alter_column('book_author', 'email', self.gf('django.db.models.fields.EmailField')(max_length=75, null=True))

        # Changing field 'Publisher.website'
        db.alter_column('book_publisher', 'website', self.gf('django.db.models.fields.URLField')(max_length=200, null=True))


    def backwards(self, orm):
        
        # Deleting field 'Book.price'
        db.delete_column('book_book', 'price')

        # Changing field 'Book.title'
        db.alter_column('book_book', 'title', self.gf('django.db.models.fields.CharField')(max_length=100))

        # Changing field 'Book.publication_date'
        db.alter_column('book_book', 'publication_date', self.gf('django.db.models.fields.DateField')())

        # Adding field 'Author.last_name'
        db.add_column('book_author', 'last_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=40), keep_default=False)

        # Adding field 'Author.first_name'
        db.add_column('book_author', 'first_name', self.gf('django.db.models.fields.CharField')(default=None, max_length=30), keep_default=False)

        # Deleting field 'Author.name'
        db.delete_column('book_author', 'name')

        # Changing field 'Author.email'
        db.alter_column('book_author', 'email', self.gf('django.db.models.fields.EmailField')(default=None, max_length=75))

        # Changing field 'Publisher.website'
        db.alter_column('book_publisher', 'website', self.gf('django.db.models.fields.URLField')(default=None, max_length=200))


    models = {
        'book.author': {
            'Meta': {'object_name': 'Author'},
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'book.book': {
            'Meta': {'object_name': 'Book'},
            'authors': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['book.Author']", 'symmetrical': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'price': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'publication_date': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 20, 12, 15, 19, 155000)'}),
            'publisher': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['book.Publisher']"}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '128'})
        },
        'book.publisher': {
            'Meta': {'object_name': 'Publisher'},
            'address': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'province': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'website': ('django.db.models.fields.URLField', [], {'max_length': '200', 'null': 'True'})
        }
    }

    complete_apps = ['book']
