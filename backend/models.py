"""
Electronics Lab Inventory - LIMS Backend
Database models using SQLAlchemy ORM
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from decimal import Decimal

# Initialize SQLAlchemy instance
db = SQLAlchemy()

class Component(db.Model):
    """
    Component model representing electronic components in the inventory
    
    This model defines the structure for storing component information
    including identification, categorization, quantity tracking, and pricing.
    """
    
    __tablename__ = 'components'
    
    # Primary key
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # Component identification
    name = db.Column(db.String(255), nullable=False, index=True,
                    comment="Human-readable component name")
    
    part_number = db.Column(db.String(100), nullable=False, unique=True, index=True,
                           comment="Unique part number for component identification")
    
    # Categorization
    category = db.Column(db.String(100), nullable=False, index=True,
                        comment="Component category (e.g., Microcontrollers, Resistors)")
    
    # Inventory tracking
    quantity = db.Column(db.Integer, nullable=False, default=0,
                        comment="Current quantity in stock")
    
    location = db.Column(db.String(100), nullable=True,
                        comment="Physical storage location (e.g., Shelf A1, Drawer B2)")
    
    # Pricing information
    unit_price = db.Column(db.Numeric(10, 2), nullable=True,
                          comment="Price per unit in USD")
    
    # Inventory management
    low_threshold = db.Column(db.Integer, nullable=False, default=0,
                             comment="Minimum quantity before low stock alert")
    
    # Metadata
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                          comment="Record creation timestamp")
    
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow,
                          onupdate=datetime.utcnow,
                          comment="Record last update timestamp")
    
    # Additional fields for future expansion
    description = db.Column(db.Text, nullable=True,
                           comment="Detailed component description")
    
    manufacturer = db.Column(db.String(100), nullable=True,
                            comment="Component manufacturer")
    
    datasheet_url = db.Column(db.String(500), nullable=True,
                             comment="URL to component datasheet")
    
    # Constraints
    __table_args__ = (
        db.CheckConstraint('quantity >= 0', name='check_quantity_non_negative'),
        db.CheckConstraint('low_threshold >= 0', name='check_threshold_non_negative'),
        db.CheckConstraint('unit_price >= 0', name='check_price_non_negative'),
    )
    
    def __init__(self, name, part_number, category, quantity=0, location=None,
                 unit_price=None, low_threshold=0, description=None,
                 manufacturer=None, datasheet_url=None):
        """
        Initialize a new Component instance
        
        Args:
            name (str): Component name
            part_number (str): Unique part number
            category (str): Component category
            quantity (int): Initial quantity (default: 0)
            location (str): Storage location (optional)
            unit_price (Decimal): Price per unit (optional)
            low_threshold (int): Low stock threshold (default: 0)
            description (str): Component description (optional)
            manufacturer (str): Manufacturer name (optional)
            datasheet_url (str): Datasheet URL (optional)
        """
        self.name = name
        self.part_number = part_number
        self.category = category
        self.quantity = quantity
        self.location = location
        self.unit_price = unit_price
        self.low_threshold = low_threshold
        self.description = description
        self.manufacturer = manufacturer
        self.datasheet_url = datasheet_url
    
    def __repr__(self):
        """
        String representation of Component instance
        """
        return f'<Component {self.part_number}: {self.name}>'
    
    def to_dict(self):
        """
        Convert Component instance to dictionary for JSON serialization
        
        Returns:
            dict: Component data as dictionary
        """
        return {
            'id': self.id,
            'name': self.name,
            'part_number': self.part_number,
            'category': self.category,
            'quantity': self.quantity,
            'location': self.location,
            'unit_price': float(self.unit_price) if self.unit_price else None,
            'low_threshold': self.low_threshold,
            'description': self.description,
            'manufacturer': self.manufacturer,
            'datasheet_url': self.datasheet_url,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'low_stock': self.is_low_stock(),
            'total_value': self.get_total_value()
        }
    
    def is_low_stock(self):
        """
        Check if component is below low stock threshold
        
        Returns:
            bool: True if quantity is at or below threshold
        """
        return self.quantity <= self.low_threshold
    
    def get_total_value(self):
        """
        Calculate total value of component stock
        
        Returns:
            float: Total value (quantity * unit_price) or None if no price
        """
        if self.unit_price is None:
            return None
        return float(self.quantity * self.unit_price)
    
    def update_quantity(self, new_quantity):
        """
        Update component quantity with validation
        
        Args:
            new_quantity (int): New quantity value
            
        Raises:
            ValueError: If quantity is negative
        """
        if new_quantity < 0:
            raise ValueError("Quantity cannot be negative")
        
        self.quantity = new_quantity
        self.updated_at = datetime.utcnow()
    
    def add_stock(self, amount):
        """
        Add stock to component quantity
        
        Args:
            amount (int): Amount to add
            
        Raises:
            ValueError: If amount is negative
        """
        if amount < 0:
            raise ValueError("Cannot add negative stock")
        
        self.quantity += amount
        self.updated_at = datetime.utcnow()
    
    def remove_stock(self, amount):
        """
        Remove stock from component quantity
        
        Args:
            amount (int): Amount to remove
            
        Raises:
            ValueError: If amount is negative or exceeds current quantity
        """
        if amount < 0:
            raise ValueError("Cannot remove negative stock")
        
        if amount > self.quantity:
            raise ValueError("Cannot remove more stock than available")
        
        self.quantity -= amount
        self.updated_at = datetime.utcnow()

# Additional models can be added here for future expansion
# Examples: User, Transaction, Supplier, etc.

class User(db.Model):
    """
    User model for authentication and authorization
    TODO: Implement when authentication is added
    """
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    def __repr__(self):
        return f'<User {self.username}>'

class Transaction(db.Model):
    """
    Transaction model for tracking inventory changes
    TODO: Implement when transaction logging is added
    """
    
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    component_id = db.Column(db.Integer, db.ForeignKey('components.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'add', 'remove', 'update'
    quantity_change = db.Column(db.Integer, nullable=False)
    previous_quantity = db.Column(db.Integer, nullable=False)
    new_quantity = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    component = db.relationship('Component', backref='transactions')
    user = db.relationship('User', backref='transactions')
    
    def __repr__(self):
        return f'<Transaction {self.id}: {self.transaction_type}>'