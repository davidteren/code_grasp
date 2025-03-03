# Branch Protection Configuration

This document provides instructions for configuring branch protection rules for the Code Grasp repository on GitHub. Since branch protection rules cannot be fully configured through files in the repository, these settings must be applied through the GitHub web interface.

## Recommended Protection Rules for the `main` Branch

1. Navigate to the repository on GitHub.
2. Go to Settings > Branches > Branch protection rules.
3. Click "Add rule".
4. Enter "main" as the branch name pattern.
5. Configure the following settings:

### Required Settings
- [x] **Require a pull request before merging**
  - [x] Require approvals (at least 1)
  - [x] Dismiss stale pull request approvals when new commits are pushed
  
- [x] **Require status checks to pass before merging**
  - [x] Require branches to be up to date before merging
  - Status checks to require:
    - Tests
    - Version-check

- [x] **Require conversation resolution before merging**

- [x] **Include administrators**

### Additional Recommended Settings
- [x] **Restrict who can push to matching branches**
  - Add repository administrators only

- [x] **Do not allow bypassing the above settings**

- [x] **Require linear history**

- [x] **Require signed commits**

## Recommended Protection Rules for the `develop` Branch

1. Follow the same steps but create a rule for "develop".
2. Configure similar but potentially less strict settings:

### Required Settings for Develop
- [x] **Require a pull request before merging**
  - [x] Require approvals (at least 1)
  
- [x] **Require status checks to pass before merging**
  - [x] Require branches to be up to date before merging
  - Status checks to require:
    - Tests

- [x] **Include administrators**

## Additional Repository Settings

For complete protection of the workflow, also consider:

1. **Default branch**: Set `develop` as the default branch for the repository
2. **Squash merging**: Enable "Automatically delete head branches" after pull requests are merged
3. **Pull Requests**: Enable "Allow merge commits" and "Allow squash merging"
