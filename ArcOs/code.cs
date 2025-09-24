[HttpGet]
[PartialOnly]
public virtual ActionResult Edit(int contentSpecificationID, bool isProjectMode)
{
    if (contentSpecificationID != -1 && contentSpecificationID <= 0)
    {
        ThrowNotAuthorizedException();
    }

    // Early authorization check - broad role-based access
    if (!_CurrentUser.HasRole(Configuration.UserRole.ContentSpecificationManager))
    {
        ThrowNotAuthorizedException();
    }

    ContentSpecificationEditViewModel_Get viewModel;

    if (contentSpecificationID == -1)
    {
        viewModel = new ContentSpecificationEditViewModel_Get
        {
            IsProjectMode = isProjectMode,
            ID = contentSpecificationID
        };
    }
    else
    {
        var contentSpecification = new ContentSpecificationRepository().GetByIDIncludeCreatedAndEditedBy(contentSpecificationID);
        EnsureNotNull(contentSpecification, "Content Type");

        // Perform fine-grained authorization
        if (contentSpecification.ProjectGUID.HasValue)
        {
            var authorizationData = new AuthorizationService().EnsureProjectAccessIsAuthorized(contentSpecification.ProjectGUID.Value, null,
            _CurrentUser.ID, Configuration.AccessType.Read, mustLock: false);
            if (!(authorizationData.UserAccessType == Configuration.AccessType.Write ||
            authorizationData.UserAccessType == Configuration.AccessType.Full))
            {
                ThrowNotAuthorizedException();
            }
        }
        else if (!isProjectMode && !contentSpecification.Is1691Item)
        {
            if (contentSpecification.OwnerAgencyID.HasValue && !_CurrentUser.HasRole(Configuration.UserRole.ContentSpecificationManager,

            contentSpecification.OwnerAgencyID.Value))
            {
                ThrowNotAuthorizedException();
            }
        }

        viewModel = Mapper.Map<ContentSpecificationEditViewModel_Get>(contentSpecification);
        viewModel.IsProjectMode = isProjectMode;
        viewModel.IsDataEditable = true; // Explicitly mark editable only after authorization passed

        PopulateEditSelectLists(viewModel);

        if (contentSpecification.Is1691Item)
        {
            PopulateVendorData(viewModel);
        }
    }

    return PartialView(viewModel);
}
