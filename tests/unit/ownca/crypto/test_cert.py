# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 Kairo de Araujo
"""
from unittest import mock
import pytest

from ownca.crypto.cert import (
    issue_cert,
    issue_csr,
    ca_sign_csr,
    _valid_cert,
    _valid_csr,
    x509,
)


@mock.patch("ownca.crypto.cert.x509")
@mock.patch("ownca.crypto.cert._valid_cert")
def test_issue_cert(
    mock__valid_certificate, mock_x509, oids_sample, fake_certificate
):

    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_certificate.return_value = fake_certificate

    cert = issue_cert(["OID"], maximum_days=1)

    assert isinstance(cert, classmethod)


@mock.patch("ownca.crypto.cert.x509")
@mock.patch("ownca.crypto.cert._valid_cert")
def test_issue_cert_with_dns_names(
    mock__valid_certificate, mock_x509, oids_sample, fake_certificate
):

    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_certificate.return_value = fake_certificate

    cert = issue_cert(
        ["OID"], maximum_days=1, dns_names=["fake-ca.com", "www.fake-ca.com"]
    )

    assert isinstance(cert, classmethod)


@mock.patch("ownca.crypto.cert.x509")
@mock.patch("ownca.crypto.cert._valid_cert")
def test_issue_cert_with_bad_dns_names(
    mock__valid_certificate, mock_x509, oids_sample, fake_certificate
):

    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_certificate.return_value = fake_certificate

    with pytest.raises(TypeError) as excinfo:

        issue_cert(["OID"], maximum_days=1, dns_names="www.fake-ca.com")

        assert "All DNS Names must to be string values." in excinfo.value

    with pytest.raises(TypeError) as excinfo:

        issue_cert(["OID"], maximum_days=1, dns_names=[123, "www.fake-ca.com"])

        assert "dns_names require a list of strings." in excinfo.value


@mock.patch("ownca.crypto.cert.x509")
@mock.patch("ownca.crypto.cert._valid_cert")
def test_issue_cert_host(
    mock__valid_certificate, mock_x509, oids_sample, fake_certificate
):

    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_certificate.return_value = fake_certificate

    cert = issue_cert(["OID"], maximum_days=1, host=True)

    assert isinstance(cert, classmethod)


@mock.patch("ownca.crypto.cert.x509")
@mock.patch("ownca.crypto.cert._valid_cert")
def test_issue_cert_without_maximum_days(
    mock__valid_certificate, mock_x509, oids_sample, fake_certificate
):

    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_certificate.return_value = fake_certificate

    with pytest.raises(ValueError) as excinfo:
        issue_cert(["OID"])

        assert "maximum_days is required" in excinfo.value


@mock.patch("ownca.crypto.cert._valid_csr")
@mock.patch("ownca.crypto.cert.x509")
def test_issue_csr(mock_x509, mock__valid_csr, oids_sample, fake_certificate):
    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_csr.return_value = fake_certificate

    csr = issue_csr(oids=["OID"])

    assert isinstance(csr, classmethod)


@mock.patch("ownca.crypto.cert._valid_csr")
@mock.patch("ownca.crypto.cert.x509")
def test_issue_csr_with_dns_names(
    mock_x509, mock__valid_csr, oids_sample, fake_certificate
):
    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_csr.return_value = fake_certificate

    csr = issue_csr(oids=["OID"], dns_names=["www.fake-ca.com"])

    assert isinstance(csr, classmethod)


@mock.patch("ownca.crypto.cert._valid_csr")
@mock.patch("ownca.crypto.cert.x509")
def test_issue_csr_with_bad_dns_names(
    mock_x509, mock__valid_csr, oids_sample, fake_certificate
):
    mock_x509.NameAttribute.return_value = oids_sample
    mock__valid_csr.return_value = fake_certificate

    with pytest.raises(TypeError) as excinfo:

        issue_csr(oids=["OID"], dns_names="www.fake-ca.com")

        assert "All DNS Names must to be string values." in excinfo.value

    with pytest.raises(TypeError) as excinfo:

        issue_csr(oids=["OID"], dns_names=[123, "www.fake-ca.com"])

        assert "dns_names require a list of strings." in excinfo.value


@mock.patch("ownca.crypto.cert.x509")
@mock.patch("ownca.crypto.cert._valid_cert")
def test_ca_sign_csr_without_maximum_days(
    mock__valid_certificate, mock_x509, oids_sample, fake_certificate
):

    mock_x509.subject_name.return_value = oids_sample
    mock__valid_certificate.return_value = fake_certificate

    with pytest.raises(ValueError) as excinfo:
        ca_sign_csr(fake_certificate, "ca_key", "csr", "key")

        assert "maximum_days is required" in excinfo.value


@mock.patch("ownca.crypto.cert.x509")
@mock.patch("ownca.crypto.cert._valid_cert")
def test_ca_sign_csr(
    mock__valid_certificate, mock_x509, oids_sample, fake_certificate
):

    mocked_csr = mock.MagicMock()
    mocked_csr.subject.return_value = True
    mocked_key = mock.MagicMock()
    mocked_key.public_key.return_value = True
    mock_x509.subject_name.return_value = oids_sample
    mock_x509.AuthorityKeyIdentifier.from_issuer_public_key.return_value = True
    mock_x509.add_extension.return_value = fake_certificate
    mock__valid_certificate.return_value = fake_certificate

    cert = ca_sign_csr(
        fake_certificate, "ca_key", mocked_csr, mocked_key, maximum_days=1
    )

    assert isinstance(cert, classmethod)


def test_valid_cert():
    fake_cert = mock.MagicMock(spec=x509.Certificate)
    assert _valid_cert(fake_cert) == fake_cert


def test_valid_cert_false():
    fake_cert = mock.MagicMock(spec=dict)
    assert _valid_cert(fake_cert) is None


def test_valid_csr():
    fake_csr = mock.MagicMock(spec=x509.CertificateSigningRequest)
    assert _valid_csr(fake_csr) == fake_csr


def test_valid_csr_false():
    fake_csr = mock.MagicMock(spec=dict)
    assert _valid_csr(fake_csr) is None
