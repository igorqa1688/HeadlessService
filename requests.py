import grpc
import headless_service_pb2_grpc
import headless_service_pb2
from functions import grpc_channel, generate_guid, generate_random_balance
from global_vars import server


def add_or_update_headless(club_guid: str, room_player_guid: str, gold_balance: int, chips_balance: int):
    nous_account_guid = generate_guid()
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.AddOrUpdateHeadlessRequest(
            club_guid=club_guid,
            room_player_guid=room_player_guid,
            gold_balance=gold_balance,
            chips_balance=chips_balance,
            nous_account_guid=nous_account_guid)
        try:
            response = stub.AddOrUpdateHeadless(request)
            return response
        except Exception as e:
            return e


def get_club_headlesses():
    club_headless = add_or_update_headless(generate_guid(), generate_guid(), 100, 50)
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.GetClubHeadlessesRequest(
            club_guid=club_headless.club_guid)
        try:
            response = stub.GetClubHeadlesses(request)
            return response
        except Exception as e:
            return e


def get_headless():
    club_headless = add_or_update_headless(generate_guid(), generate_guid(), 70, 999)
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.GetHeadlessRequest(
            nous_account_guid=club_headless.nous_account_guid,
            room_player_guid=club_headless.room_player_guid,
            club_guid=club_headless.club_guid
        )
        try:
            response = stub.GetHeadless(request)
            return response
        except Exception as e:
            return e


def get_headless_by_one_param(nous_account_guid: None, room_player_guid: None, club_guid: None) -> str:
    with grpc.insecure_channel(server) as channel:
        stub = headless_service_pb2_grpc.HeadlessServiceStub(channel)
        request = headless_service_pb2.GetHeadlessRequest(
            nous_account_guid=nous_account_guid,
            room_player_guid=room_player_guid,
            club_guid=club_guid
        )
        try:
            response = stub.GetHeadless(request)
            return response
        except Exception as e:
            return e


if __name__ == "__main__":
    print(add_or_update_headless(generate_guid(), generate_guid(), 100, 50))
    print(get_club_headlesses())
    print(get_headless())
