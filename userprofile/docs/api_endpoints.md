# API Endpoints

| URL Pattern | HTTP Method | View / View Name | Description |
|-------------|-------------|------------------|-------------|
| `/api/user/` | GET / POST | `UserListCreateView` / `user-list-create` | List all users or create a new user |
| `/api/user/detail/` | GET / PUT / PATCH | `SelfUserDetailView` / `self-user-detail` | Retrieve or update the logged-in user's details |
| `/api/user/<int:id>/details/` | GET / PUT / PATCH / DELETE | `UserRetrieveUpdateDeleteView` / `user-retrieve-update-delete` | Retrieve, update, or delete a specific user by ID |
| `/api/user/change-password/` | POST | `ChangePasswordView` / `user-change-password` | Change password for the logged-in user |
| `/api/user/admin/<int:id>/reset-password/` | POST | `ResetPasswordView` / `user-reset-password` | Admin resets password for a specific user |
| `/api/user/userprofile/` | GET / POST | `UserProfileListCreateView` / `userprofile-list-create` | List all user profiles or create a new profile |
| `/api/user/userprofile/details/` | GET / PUT / PATCH | `SelfUserProfileDetailUpdateView` / `self-profile-detail-update` | Retrieve or update the logged-in user's profile |
| `/api/user/admin/userprofile/<int:id>/details/` | GET / PUT / PATCH / DELETE | `SuperUserProfileDetailUpdateDeleteView` / `super-userprofile-detail-update-delete` | Superuser retrieves, updates, or deletes a user profile by ID |
| `/api/user/role-choices/` | GET | `GetRoleChoices` / `get-role-choices` | Get available user role choices |
| `/api/user/getusers/` | GET | `GetUsers` / `get-users` | Retrieve a filtered list of users |