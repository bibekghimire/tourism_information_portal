# Userprofile and User Management
## User
- username
- password

## `CleanValidatedModel` (Abstract Base Model)

The `CleanValidatedModel` is an **abstract base model** that provides:  
- Automatic **validation** using `full_clean()` before saving, unless validation was already done externally (e.g., by a DRF serializer).  
- Standard **audit fields** for tracking creation and modification.  

This ensures that model instances are always validated before persistence, while avoiding redundant validation when already handled by serializers.

---

### Fields

| Field | Type | Description |
|-------|------|-------------|
| **_validated** | `bool` (internal flag) | Indicates whether the instance has already been validated. Defaults to `False`. |
| **created_at** | `DateTimeField(auto_now_add=True)` | Timestamp when the object was created. |
| **created_by** | `ForeignKey(User, on_delete=PROTECT, editable=False, null=True, related_name='userprofiles_created')` | The user who created the object. Non-editable. |
| **modified_by** | `ForeignKey(User, on_delete=PROTECT, null=True, blank=True, related_name='modified_profiles')` | The user who last modified the object. |
| **last_modified** | `DateTimeField(auto_now=True)` | Timestamp of the last modification. |

---

### Methods

#### `save(self, *args, **kwargs)`
Custom `save` implementation:  
1. If `_validated` is `False` → run `full_clean()` to validate the instance.  
2. Otherwise → skip validation (useful when serializers have already validated the data).  
3. Calls `super().save()` to persist the model.  

This mechanism ensures consistent validation, but avoids duplicate validation when using Django REST Framework serializers.

---

## UserProfile model
The `UserProfile` model extends `CleanValidatedModel` and stores additional information about a Django `User`.

### fields

| Field | Type | Description | Validation |
|-------|------|-------------|------------|
| first_name | CharField(max_length=32) | User’s first name | No whitespace, name_validator |
| last_name | CharField(max_length=32) | User’s last name | No whitespace, name_validator |
| display_name | CharField(max_length=65, null=True, blank=True) | Display name, defaults to full name if not provided | No whitespace, name_validator |
| email | EmailField(unique=True) | Unique email address | No whitespace |
| phone_number | CharField(max_length=10, unique=True) | Unique phone number | No whitespace, phone_number_validator |
| date_of_birth | DateField | Date of birth | age_validator |
| user | OneToOneField(User, on_delete=PROTECT) | Links to Django’s built-in User | Protected from deletion |
| profile_picture | ImageField(blank=True, upload_to=user_directory_path) | User’s profile picture | profile_picture_validator |
| role | CharField(max_length=2, choices=RoleChoices) | User’s role (Admin, Staff, Creator, etc.) | Must be from RoleChoices |
| public_id | UUIDField(default=uuid.uuid4, editable=False, unique=True) | Public unique identifier | Auto-generated |

### Methods and Properties

- **`__str__()`**: Returns a readable string in the format `<first_name> <last_name>: <role>, <id>: <username>`.

- **`full_name`**: Property that returns the user’s full name by concatenating `first_name` and `last_name`. Used to auto-populate `display_name` if empty.  
  ```python
  @property
  def full_name(self):
      return f'{self.first_name} {self.last_name}'

- **`save()`**: Custom save method that deletes the old profile picture if updated, auto-fills display_name from full_name if empty, and then calls the parent save(). Ensures no orphan files and that display_name is always populated.

### Example usage
```
user_profile = UserProfile.objects.create(
    user=some_user,
    first_name="Alice",
    last_name="Smith",
    email="alice@example.com",
    phone_number="9812345678",
    date_of_birth="1995-08-20",
    role="CR"
)

print(user_profile.full_name)    # "Alice Smith"
print(user_profile.display_name) # "Alice Smith"

```
